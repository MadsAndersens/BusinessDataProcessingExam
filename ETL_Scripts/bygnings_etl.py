import pandas as pd 
import os
from utils.bbr_data import *
from utils.database import PostgresDB


# Define the ETL script, that runs the ETL process for a given municipality
class BuildingETL:
  
    def __init__(self, municipality_id: str):
        self.municipality_id = municipality_id
        self.adress_csv_path = f'Data/Adress_data/Adress_data_{self.municipality_id}.csv'
        self.dawa_data = self.fetch_adress_data()

        self.bbr_data = None
        self.db = None

    def fetch_adress_data(self):
        if self.adress_csv_path not in os.listdir('Data/Adress_data'):
            url = f'https://api.dataforsyningen.dk/adgangsadresser?kommunekode={self.municipality_id}&format=csv'
            dawa_data = pd.read_csv(url)
            dawa_data.to_csv(self.adress_csv_path, index=False)
        else: 
            dawa_data = pd.read_csv(self.adress_csv_path)

        return dawa_data

    def get_bbr_data(self, adgangs_adresse_id: str) -> List[Building]:
        #Lookup the data from the BBR API
        bbr_data = lookup_bbr_data(adgangs_adresse_id)

        #Load the data into the pydantic model
        bbr_data = load_pydantic_model(bbr_data)

        #Check if the status of the building is active
        bbr_data = [item for item in bbr_data if item.status == '6']

        return bbr_data
    
    def run_etl(self) -> None:
        
        for idx, row in self.dawa_data.iterrows():
            adgangs_adresse_id = row['adgangspunktid']
            lattitude, longitude = row['vejpunkt_x'], row['vejpunkt_y']

            #Get the BBR data for the given adgangs_adresse_id
            bbr_data = self.get_bbr_data(adgangs_adresse_id)

            # Write the data to the database
            print(bbr_data)
            break
            #self.write_to_database(bbr_data, lattitude, longitude)
    
    def write_to_database(self, bbr_data: List[Building], lattitude: float, longitude: float) -> None:
        # Initialize the database connection
        self.db = PostgresDB("BuildingData","Mads", os.environ['DB_PASSWORD'])

        try:
            self.db.connect()

            for building in bbr_data:
                # Example: Insert a row into the table
                insert_query = """
                INSERT INTO "Buildings" (
                  "Building_Id",
                  "construction_year",
                  "ussage_code",
                  "collected_area",
                  "industry_area",
                  "foot_print_area",
                  "outer_wall_meterial",
                  "roof_material",
                  "floors",
                  "heating_source_id",
                  "shelter_space",
                  "lattitude",
                  "longitude"
                ) VALUES ( 
                    %(Building_Id)s,
                    %(construction_year)s,
                    %(ussage_code)s,
                    %(collected_area)s,
                    %(industry_area)s,
                    %(foot_print_area)s,
                    %(outer_wall_meterial)s,
                    %(roof_material)s,
                    %(floors)s,
                    %(heating_source_id)s,
                    %(shelter_space)s,
                    %(lattitude)s,
                    %(longitude)s
                    );
                    """
                params = {
                    "Building_Id": building.id_lokalId,
                    "construction_year": building.opførelsesår,
                    "ussage_code": building.bygningensAnvendelse,
                    "collected_area": building.samletBygningsareal,
                    "industry_area": building.erhvervsareal,
                    "foot_print_area": building.bebyggetAreal,
                    "outer_wall_meterial": building.ydermurkonsistens,
                    "roof_material": building.tagdækningsmateriale,
                    "floors": building.etagerAntal,
                    "heating_source_id": building.opvarmningsform,
                    "shelter_space": building.tagkonstruktion,
                    "lattitude": lattitude,
                    "longitude": longitude
                }
                self.db.execute_query(insert_query, params)

        finally:
            self.db.close()
            print("Data successfully written to database.")
        

