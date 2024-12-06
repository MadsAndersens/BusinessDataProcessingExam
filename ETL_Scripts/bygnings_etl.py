import pandas as pd 
import os
from utils.bbr_data import *
from utils.database import PostgresDB
from tqdm import tqdm


# Define the ETL script, that runs the ETL process for a given municipality
class BuildingETL:
  
    def __init__(self, municipality_id: str):
        self.municipality_id = municipality_id
        self.adress_csv_path = f'Data/Adress_data/Adress_data_{self.municipality_id}.csv'
        self.dawa_data = self.fetch_adress_data()
        self.db = PostgresDB("BuildingData","Mads", os.environ['DB_PASSWORD'])
        self.bbr_data = None

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
        self.db.connect()
        for idx, row in tqdm(self.dawa_data.iterrows(), total=len(self.dawa_data)):
            adgangs_adresse_id = row['adgangspunktid']
            lattitude, longitude = row['vejpunkt_x'], row['vejpunkt_y']

            #Get the BBR data for the given adgangs_adresse_id
            bbr_data = self.get_bbr_data(adgangs_adresse_id)

            # Write the data to the database
            self.write_to_database(bbr_data, lattitude, longitude)
            

            if idx == 10:
                break

        self.db.close()
    
    def write_to_database(self,
                          bbr_data: List[Building],
                          lattitude: float,
                          longitude: float) -> None:
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
                    asbestos_code
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
                    %(asbestos_code)s
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
                            "lattitude": lattitude
                            }
                self.db.execute_query(insert_query, params)

        # Write to error log for the db log
        except Exception as e:
            self.db.write_error_log(f"Building ETL Failed with error: {e}")