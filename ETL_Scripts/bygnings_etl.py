import pandas as pd 
import os
from time import sleep
from tqdm import tqdm
from pydantic import BaseModel

#Internal imports: 
from utils.bbr_data import *
from utils.database import PostgresDB
from utils.dawa_data import *
from utils.school_utils import lookup_nearest_school, School
from utils.public_transport import get_nearest_station


# Define the ETL script, that runs the ETL process for a given municipality
class BuildingETL:
  
    def __init__(self, municipality_id: str):
        self.municipality_id = municipality_id
        self.adress_csv_path = f'Data/Adress_data/Adress_data_{self.municipality_id}.csv'
        self.fetch_adress_data()
        self.db = PostgresDB("BuildingData","Mads", os.environ['DB_PASSWORD'])
        self.bbr_data = None

    def fetch_adress_data(self) -> None:
        if f'Adress_data_{self.municipality_id}.csv' not in os.listdir('Data/Adress_data'):
            url = f'https://api.dataforsyningen.dk/adgangsadresser?kommunekode={self.municipality_id}&format=csv'
            dawa_data = pd.read_csv(url) # Fetch the data and save it to a csv file
            dawa_data.to_csv(self.adress_csv_path, index=False)

    def get_bbr_data(self, adgangs_adresse_id: str) -> List[Building]:
        #Lookup the data from the BBR API
        bbr_data = lookup_bbr_data(adgangs_adresse_id)

        #Load the data into the pydantic model
        bbr_data = load_pydantic_model(bbr_data)

        #Check if the status of the building is active
        bbr_data = [item for item in bbr_data if item.status == '6']

        return bbr_data
    
    def get_closest_school(self, lattitude: float, longitude: float) -> str:
        #Lookup the data from the csv file with schools gathered from the schools pipeline: 
        school = lookup_nearest_school(lattitude, longitude)
        return school

    def run_etl(self) -> None:
        self.db.connect()
        for idx, row in tqdm(enumerate(load_adress_data(self.adress_csv_path))):
            adgangs_adresse_id = row.id
            lattitude, longitude = row.vejpunkt_x, row.vejpunkt_y
            road_name = row.adresseringsvejnavn
            house_number = row.husnr
            postal_code = row.postnr
            postal_code_name = row.postnrnavn

            #Get the BBR data for the given adgangs_adresse_id
            bbr_data = self.get_bbr_data(adgangs_adresse_id)

            # Check if the data is empty
            if len(bbr_data) == 0:
                continue
            
            # Get the closest school to the building
            closest_school = self.get_closest_school(lattitude, longitude)

            # Get the closest stations to the building
            metro_station = get_nearest_station(lattitude, longitude, 'metro')
            s_train_station = get_nearest_station(lattitude, longitude, 'train')
            bus_station = get_nearest_station(lattitude, longitude, 'bus')
            tram_station = get_nearest_station(lattitude, longitude, 'tram')

            # Write the data to the database
            self.write_to_database( adgangs_adresse_id,
                                    bbr_data,
                                    lattitude,
                                    longitude,
                                    house_number,
                                    road_name,
                                    postal_code,
                                    metro_station,
                                    s_train_station,
                                    bus_station,
                                    tram_station,
                                    closest_school
                                    )
            
            # For every 100 rows take a 5 second break
            if idx % 100 == 0:
                sleep(5)

        self.db.close()
    
    def write_to_database(self,
                          adgangs_adresse_id: str,
                          bbr_data: List[Building],
                          lattitude: float,
                          longitude: float,
                          house_number: int,
                          road_name: str,
                          postal_code: int,
                          metro_station: BaseModel,
                          s_train_station: BaseModel,
                          bus_station: BaseModel,
                          tram_station: BaseModel,
                          closest_school: School
                        ) -> None:
        # Write the data to the database
        try:
            for building in bbr_data:
                # Example: Insert a row into the table
                insert_query = """
                INSERT INTO "Buildings" (
                    building_id,
                    construction_year,
                    ussage_code,
                    collected_area,
                    industry_area,
                    housing_area,
                    foot_print_area,
                    outer_wall_meterial,
                    roof_material,
                    water_supply,
                    drainage,
                    floors,
                    heating_source_id,
                    alternate_heating_source_id,
                    carport,
                    plot_id,
                    municipality_id,
                    longitude,
                    lattitude,
                    asbestos_code,
                    house_number,
                    road_name,
                    postal_code
                ) VALUES ( 
                    %(building_id)s,
                    %(construction_year)s,
                    %(ussage_code)s,
                    %(collected_area)s,
                    %(industry_area)s,
                    %(housing_area)s,
                    %(foot_print_area)s,
                    %(outer_wall_meterial)s,
                    %(roof_material)s,
                    %(water_supply)s,
                    %(drainage)s,
                    %(floors)s,
                    %(heating_source_id)s,
                    %(alternate_heating_source_id)s,
                    %(carport)s,
                    %(plot_id)s,
                    %(municipality_id)s,
                    %(longitude)s,
                    %(lattitude)s,
                    %(asbestos_code)s,
                    %(house_number)s,
                    %(road_name)s,
                    %(postal_code)s
                );
                """
                params = {
                            "building_id": building.id_lokalId,
                            "construction_year": building.byg026Opførelsesår,
                            "ussage_code": building.byg021BygningensAnvendelse,
                            "collected_area": building.byg038SamletBygningsareal,
                            "housing_area": building.byg039BygningensSamledeBoligAreal,
                            "foot_print_area": building.byg041BebyggetAreal,
                            "industry_area": building.byg040BygningensSamledeErhvervsAreal,
                            "outer_wall_meterial": building.byg032YdervæggensMateriale,
                            "roof_material": building.byg033Tagdækningsmateriale,
                            "water_supply": building.byg030Vandforsyning,
                            "drainage": building.byg031Afløbsforhold,
                            "floors": building.byg054AntalEtager,
                            "heating_source_id": building.byg056Varmeinstallation,
                            "alternate_heating_source_id": building.byg058SupplerendeVarme,
                            "carport": building.byg043ArealIndByggetCarport,
                            "plot_id": building.grund,
                            "municipality_id": building.kommunekode,
                            "asbestos_code": building.byg036AsbestholdigtMateriale,
                            "longitude": longitude,
                            "lattitude": lattitude,
                            "house_number": house_number,
                            "road_name": road_name,
                            "postal_code": postal_code
                            }
                self.db.execute_query(insert_query, params)

        # Write to error log for the db log
        except Exception as e:
            self.db.write_error_log(f"Building ETL Failed with error: {e}")