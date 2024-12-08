import pandas as pd
import os
import pandas as pd
import requests
import json
import os
from haversine import haversine, Unit
from pydantic import BaseModel, Field
from typing import Optional


#Define pydantic model for the school data
class School(BaseModel):
    school_id: int = Field(..., description="The unique identifier for the school")
    school_name: str = Field(..., description="The name of the school")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="The longitude of the school, must be between -180 and 180")
    latitude: float = Field(..., ge=-90.0, le=90.0, description="The latitude of the school, must be between -90 and 90")
    ten_yr_avg: float = Field(..., alias="10_yr_avg", description="The 10-year average value for the school")

    class Config:
        allow_population_by_field_name = True


def lookup_nearest_school(lattitude: float, longitude: float) -> School:
    """
    Lookup the closest school to a given lattitude and longitude.
    
    :param lattitude: Lattitude of the location
    :param longitude: Longitude of the location
    :return: DataFrame containing the school data
    """
    #Lookup the data from the DAWA API
    school_csv = 'Data/school_data.csv'

    if 'school_data.csv' not in os.listdir('Data'):
        school_pipe = SchoolsPipeline()
        school_data = school_pipe.run_pipeline()
    else:
        school_data = pd.read_csv(school_csv)
    
    #Get the closest school by calculating the distance to each school from the given location
    distances = []
    for idx, row in school_data.iterrows():
        school_lattitude = row.latitude
        school_longitude = row.longitude
        school_location = (school_lattitude, school_longitude)
        location = (lattitude, longitude)
        distance = haversine(school_location, location, unit=Unit.METERS)
        distances.append(distance)

    #Add the distances to the DataFrame and sort by distance
    school_data['distance'] = distances
    school_data = school_data.sort_values('distance')

    # Get the first school in the sorted list
    closest_school = school_data.iloc[0]

    closest_school = closest_school.to_dict()
    school_model = School(**closest_school)
    return school_model

class ParentPipe: 

  def __init__(self,table_name):
    self.table_name = table_name
  
  def run_pipeline(self):
    pass
  
class SchoolsPipeline(ParentPipe):

    def __init__(self):
        super().__init__('Schools')
        self.api_url = "https://api.uddannelsesstatistik.dk/Api/v1/statistik"
        self.api_key = os.getenv("SCHOOL_API_KEY")
  
    def run_pipeline(self):
        query = {
            "område": "GS",
            "emne": "KARA",
            "underemne": "KARAGNS",
            "nøgletal": [
                "Antal elever med karakter eller anden status i prøver",
                "Gennemsnit - Obl. prøver"
            ],
            "detaljering": [
                "[Institution].[Beliggenhedskommunenummer]",
                "[Institution].[Institution]",
                "[Institution].[Institution Beliggenhedskommune]",
                "[Institution].[Institutionsnummer]",
                "[Klassetrin].[Klassetrin]",
                "[Klassetype].[Klassetype]",
                "[Skoleår].[Skoleår]"
            ],
            "indlejret": False,
            "tomme_rækker": False,
            "formattering": "json",
            "side": 1
        }
                    
        headers = {"content-type": "application/json", "authorization": "Bearer %s" % self.api_key}

        all_data = []
        page_number = 1

        while True:
            query["side"] = page_number
            response = requests.post(self.api_url, data=json.dumps(query), headers=headers)
            
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                break
            
            data = response.json()
            
            # Break if no more data is returned
            if not data:
                break
            
            all_data.extend(data)
            page_number += 1  # Move to the next page

        # Convert to DataFrame
        skole_df = pd.DataFrame(all_data)
        print(f"Total rows fetched: {len(skole_df)}")


        # Kommuner:
        belig = skole_df["[Institution].[Institution Beliggenhedskommune].[Institution Beliggenhedskommune]"].value_counts()
        kommuner = ["København",
                    "Gladsaxe",
                    "Gentofte",
                    "Frederiksberg",
                    "Lyngby-Taarbæk",
                    "Taarbæk",
                    "Lyngby",
                    "Hvidovre",
                    "Ballerup", 
                    "Brøndby",
                    "Rødovre",
                    "Furesø",
                    "Tårnby",
                    "Albertslund",
                    "Høje-Taastrup",
                    "Vallensbæk",
                    "Ishøj",
                    "Herlev",
                    "Glostrup",     
                    "Egedal"]

        int_kom = skole_df[
            skole_df["[Institution].[Institution Beliggenhedskommune].[Institution Beliggenhedskommune]"].isin(kommuner)]

        years = ["2013/2014", "2014/2015", "2015/2016", "2016/2017","2017/2018", "2018/2019", "2019/2020", "2020/2021", 
                "2021/2022", "2022/2023"]

        int_years = int_kom[
            int_kom["[Skoleår].[Skoleår].[Skoleår]"].isin(years)]

        niende = ["9"]
        int_klasse_trin = int_years[
            int_years["[Klassetrin].[Klassetrin].[Klassetrin]"].isin(niende)]

        #Fikser rækkerne på df:

        skoler = int_klasse_trin

        skoler.reset_index(drop=True, inplace=True)

        #Laver gennemsnit. Dette burde sørge for at de skoler med manglende info tages hensyn til. F.eks hvis en skole har alle
        # 10 årgange perfekt, men hvis den kun har 3 så divideres det totale sum med 3 og ikke 10:

        #Men først skal jeg ændre komma til punktum i df'en.

        skoler['Gennemsnit - Obl. prøver'] = skoler['Gennemsnit - Obl. prøver'].str.replace(',', '.', regex=False)
        skoler['Gennemsnit - Obl. prøver'] = pd.to_numeric(skoler['Gennemsnit - Obl. prøver'])

        skoler['Historisk Gennemsnit'] = skoler.groupby("[Institution].[Institution].[Institution]")["Gennemsnit - Obl. prøver"].transform('mean').round(1)

        cols_to_drop = ['[Klassetype].[Klassetype].[Klassetype]',
                'Antal elever med karakter eller anden status i prøver']
                
        skoler = skoler.drop(columns = cols_to_drop) 

        skoler = skoler.pivot_table(
            index =['[Institution].[Beliggenhedskommunenummer].[Beliggenhedskommunenummer]',
                '[Institution].[Institution].[Institution]',
                '[Institution].[Institution Beliggenhedskommune].[Institution Beliggenhedskommune]',
                '[Institution].[Institutionsnummer].[Institutionsnummer]',
                '[Klassetrin].[Klassetrin].[Klassetrin]',
                'Historisk Gennemsnit'
            ],
            columns =  '[Skoleår].[Skoleår].[Skoleår]',
            values = 'Gennemsnit - Obl. prøver',
            aggfunc= 'first'
        ).reset_index()

        skoler.rename(columns={
            '[Institution].[Beliggenhedskommunenummer].[Beliggenhedskommunenummer]': 'municipality_id',
            '[Institution].[Institution].[Institution]':'school_name',
            '[Institution].[Institution Beliggenhedskommune].[Institution Beliggenhedskommune]': 'municipality_name',
            '[Institution].[Institutionsnummer].[Institutionsnummer]': 'school_id',
            '[Klassetrin].[Klassetrin].[Klassetrin]':'grade', 
            'Historisk Gennemsnit': '10_yr_avg',
            '2013/2014':'2013/2014', 
            '2014/2015':'2014/2015', 
            '2015/2016':'2015/2016',
            '2016/2017':'2016/2017', 
            '2017/2018':'2017/2018',
            '2018/2019':'2018/2019',
            '2019/2020':'2019/2020',
            '2020/2021':'2020/2021',
            '2021/2022':'2021/2022', 
            '2022/2023':'2022/2023'
        }, inplace=True)

        #Sub index, we dont need the above data afterall
        col_order=['school_name', 'school_id', '10_yr_avg']

        skoler=skoler[col_order]
        skoler = self._add_location(skoler)

        #Write to the csv file: 
        skoler.to_csv('Data/Entities_database/schools.csv', index=False)

        return pd.read_csv('Data/Entities_database/schools.csv', dtype = {'school_id': str, 'municipality_id': str})
  
    def _add_location(self, skoler):
        skoler = skoler.copy()
        skoler['denmark_school_name'] = skoler['school_name']+ ', Denmark'

        # Assuming skole_navne is your DataFrame and 'Skole med Danmark' is the column with institution names
        inst_navn = skoler['denmark_school_name'].tolist()

        API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
        
        def get_geocode_data(inst_navn, API_KEY):
            base_url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                'address': inst_navn,
                'key': API_KEY
            }
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK':
                    result = data['results'][0]
                    address = result['formatted_address']
                    latitude = result['geometry']['location']['lat']
                    longitude = result['geometry']['location']['lng']
                    return address, latitude, longitude
                else:
                    return "Address not found", None, None
            else:
                return "API request failed", None, None

        # Lists to store the results
        addresses = []
        latitudes = []
        longitudes = []

        # Loop through the institution names and get the corresponding geocode data
        for name in inst_navn:
            address, lat, lng = get_geocode_data(name, API_KEY)
            addresses.append(address)
            latitudes.append(lat)
            longitudes.append(lng)

        # Add the data to the DataFrame
        skoler['Address'] = addresses
        skoler['Latitude'] = latitudes
        skoler['Longitude'] = longitudes

        #Find the schools that are missing addresses, needed some manual lookups
        skoler.loc[skoler['school_name'] == 'Basen',['Address', 'Longitude', 'Latitude']] = [
            'Carl Nielsens Allé 15 C, 1. sal,  2100 København Ø, Denmark', 55.71307681702744, 12.57975872709277]
        skoler.loc[skoler['school_name'] == 'Behandlingsskolen Pilen ApS',['Address', 'Longitude', 'Latitude']] = [
            'Leifsgade 33, 1., 2300 København S, Denamrk', 55.66283697996421, 12.577824798254762]
        skoler.loc[skoler['school_name'] == 'Copenhagen City School',['Address', 'Longitude', 'Latitude']] = [
            'Gammel Kongevej 15 C, 1610 København V, Denmark', 55.67348882363176, 12.557627298255191]
        skoler.loc[skoler['school_name'] == 'Dagbehandlingsskolen Fortuna',['Address', 'Longitude', 'Latitude']] = [
            'Lersø Parkallé 109, 2100 København Ø, Denmark', 55.71491619719024, 12.546339569420649]
        skoler.loc[skoler['school_name'] == 'Dagbehandlingsskolen Fyrtårnet',['Address', 'Longitude', 'Latitude']] = [
            'Linde Allé 53, 2720 Vanløse, Denmark', 55.681177766415274, 12.48531016941935]
        skoler.loc[skoler['school_name'] == 'Den Specialpædagogiske Dagbehandlingsinstitution Sputnik 1 ApS',['Address', 'Longitude', 'Latitude']] = [
            'Klædemålet 9, 2100 København Ø, Denmark', 55.71368659947262, 12.547104240584517]
        skoler.loc[skoler['school_name'] == 'Den Specialpædagogiske Dagbehandlingsinstitution Sputnik 11 ApS',['Address', 'Longitude', 'Latitude']] = [
            'Tøndergade 16, 3., 1752 København V, Denmark', 55.670220329539355, 12.54285286941896]
        skoler.loc[skoler['school_name'] == 'Distrikt Ørestad',['Address', 'Longitude', 'Latitude']] = [
            'Arne Jacobsens Allé 21, 2300 København S, Denmark', 55.631037566119396, 12.582227384761822]
        skoler.loc[skoler['school_name'] == 'Iqra Privatskole',['Address', 'Longitude', 'Latitude']] = [
            'Hermodsgade 28, 2200 København N, Denmark', 55.70431918089916, 12.55166699825633]
        skoler.loc[skoler['school_name'] == 'Karlsvognen',['Address', 'Longitude', 'Latitude']] = [
            'Leifsgade 33, 4., 2300 København S, Denmark', 55.662903548893, 12.577846255926943]
        skoler.loc[skoler['school_name'] == 'Københavns Kommunes Ungdomsskole Prøveforberedende tilbud',['Address', 'Longitude', 'Latitude']] = [
            'Hovmestervej 30, 2400 København NV, Denmark', 55.71037436123636, 12.531313811748323]
        skoler.loc[skoler['school_name'] == 'Sankt Annæ Gymnasiums Grundskole',['Address', 'Longitude', 'Latitude']] = [
            'Sjælør Boulevard 135, 2500 Valby, Denmark', 55.65615044792661, 12.525797269418428 ]
        skoler.loc[skoler['school_name'] == 'Polaris, Nordre Fasanvej',['Address', 'Longitude', 'Latitude']] = [
            'Nordre Fasanvej 99, 2000 Frederiksberg, Denmark', 55.689047883631034, 12.52829289825575]
        skoler.loc[skoler['school_name'] == 'Baltorpskolen - Distriktsskole',['Address', 'Longitude', 'Latitude']] = [
            'Platanbuen 1, 2750 Ballerup, Denmark', 55.72594843473577, 12.343888082912768]
        skoler.loc[skoler['school_name'] == 'Skovvejens Skole - Distriktsskole',['Address', 'Longitude', 'Latitude']] = [
            'Egebjergvang 80, 2750 Ballerup, Denmark', 55.74864714226515, 12.379141984766274]
        skoler.loc[skoler['school_name'] == 'Unge2-projektet',['Address', 'Longitude', 'Latitude']] = [
            'Malmparken 10, 2750 Ballerup, Denmark', 55.725402909492516, 12.384790240584934]
        skoler.loc[skoler['school_name'] == 'Den Specialpædagogiske Dagbehandlingsinstitution Sputnik 6 ApS',['Address', 'Longitude', 'Latitude']] = [
            'Grusbakken 5, 2820 Gentofte, Denmark', 55.758475179372894, 12.499782040586219]
        skoler.loc[skoler['school_name'] == 'Gentofte Kommunes Ungdomsskole',['Address', 'Longitude', 'Latitude']] = [
            'Bregnegårdsvej 21 B, 2900 Hellerup, Denmark', 55.74295456316987, 12.567512511749447]
        skoler.loc[skoler['school_name'] == 'Bagsværd Gymnasiums Grundskole',['Address', 'Longitude', 'Latitude']] = [
            'Aldershvilevej 138, 2880 Bagsværd, Denmark', 55.76464582078441, 12.451406140586373]
        skoler.loc[skoler['school_name'] == 'Fløng Skole',['Address', 'Longitude', 'Latitude']] = [
            'Fløng Byvej 24, 2640 Hedehusene, Denmark', 55.6619439954884, 12.178460082910444]
        skoler.loc[skoler['school_name'] == 'Specialskolen Tårnbygård',['Address', 'Longitude', 'Latitude']] = [
            ' Englandsvej 392, 2770 Kastrup, Denmark', 55.6192804576735, 12.605038469417066]
        skoler.loc[skoler['school_name'] == 'Egedal Skole',['Address', 'Longitude', 'Latitude']] = [
            'Bækkegårdsplads 2, 3650 Ølstykke, Denmark', 55.777917444484295, 12.180400713603445]
        skoler.loc[skoler['school_name'] == 'Fyrtårnet Stenløse ApS',['Address', 'Longitude', 'Latitude']] = [
            'Skolevej 10, 3660 Stenløse, Denmark', 55.76879105578486, 12.209195527094973]
        skoler.loc[skoler['school_name'] == 'Stenløse Privatskole',['Address', 'Longitude', 'Latitude']] = [
            'Dam Holme 5, 3660 Stenløse, Denmark', 55.77543357601206, 12.197453311750717]
        skoler.loc[skoler['school_name'] == 'Stenløse Skole',['Address', 'Longitude', 'Latitude']] = [
            'Præstegårdsvej 30, 3660 Stenløse, Denmark', 55.76395527004314, 12.197435311750287]
        skoler.loc[skoler['school_name'] == 'Ølstykke Skole',['Address', 'Longitude', 'Latitude']] = [
            'Skelbækvej 8A, 3650 Ølstykke, Denmark', 55.802276304786375, 12.151628455932231]

        skoler['road_name'] = skoler['Address'].str.extract(r'^(.*?)(\d)')[0]
        skoler['school_building_number'] = skoler['Address'].str.extract(r'(\d.*)$')[0]
        skoler['postal_code'] = skoler['school_building_number'].str.extract(r'(\d{4}.*)')
        skoler['school_building_number'] = skoler['school_building_number'].str.replace(r',?\s*\d{4}.*', '', regex=True)
        skoler['postal_code'] = skoler['postal_code'].str.replace(r'\D', '', regex=True)

        skoler['postal_code'] = skoler['postal_code'].astype(str).str.slice(0, 4)

        mapping = {
            (1000, 1473): 'København K' , (1500, 1799):'København V' , (1800, 1999):'Frederiksberg C', 
            2000: 'Frederiksberg', 2100: 'København Ø', 2150: 'Nordhavn', 2200: 'København N', 
            2300: 'København S', 2400: 'København NV', 2450: 'København SV', 2500: 'Valby',
            2600: 'Glostrup', 2605: 'Brøndby', 2610: 'Rødovre', 2620: 'Albertslund', 2625: 'Vallensbæk',
            2630: 'Taastrup', 2635: 'Ishøj',  2640: 'Hedehusene', 2650: 'Hvidovre', 2660: 'Brøndby Strand', 
            2665: 'Vallensbæk Strand', 2670: 'Greve', 2680: 'Solrød Strand', 2700: 'Brønshøj',
            2720: 'Vanløse', 2730: 'Herlev', 2740: 'Skovlunde', 2750: 'Ballerup', 2765: 'Smørum', 
            2760 :'Måløv', 2791: 'Dragør', 2770: 'Kastrup', 2800: 'Kongens Lyngby', 2820: 'Gentofte', 
            2830: 'Virum', 2840: 'Holte', 2850: 'Nærum', 2860: 'Søborg', 2860: 'Søborg', 2870: 'Dyssegård', 
            2880: 'Bagsværd', 2900: 'Hellerup', 2920: 'Charlottenlund', 2942: 'Skodsborg', 
            2930: 'Klampenborg', 2950: 'Vedbæk', 2960: 'Rungsted Kyst', 2970: 'Hørsholm', 2980: 'Kokkedal', 
            2990: 'Nivå', 3000: 'Helsingør', 3050: 'Humlebæk', 3060: 'Espergørde', 3070: 'Snekkersten',
            3080: 'Tikøb', 3100: 'Hornbæk', 3400: 'Hillerød', 3500: 'Værløse', 3520: 'Farum', 
            3600: 'Frederikssund', 3650: 'Ølstykke', 3660: 'Stenløse', 

        }

        skoler['postal_code'] = pd.to_numeric(skoler['postal_code'], errors='coerce')

        def map_postal_code(post_code):
            for key, value in mapping.items():
                if isinstance(key, tuple):  # If the key is a tuple representing a range
                    if key[0] <= post_code <= key[1]:
                        return value
                elif post_code == key:
                    return value
            return 'Unknown'  # Default if not found in mapping

        # Apply the mapping function to create the 'postal_name' column
        skoler['postal_name'] = skoler['postal_code'].apply(map_postal_code)
        skoler = skoler.drop(index=[62,96]).reset_index(drop=True)

        skoler = skoler.drop(['denmark_school_name'], axis=1)
        skoler = skoler.rename(columns = {'Address': 'address', 'Latitude': 'latitude', 'Longitude': 'longitude'})
        skoler['municipality_id'] = skoler['municipality_id'].astype(str).str.zfill(4)
        return skoler