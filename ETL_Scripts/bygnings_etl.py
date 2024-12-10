import pandas as pd 
import os
from time import sleep
from tqdm import tqdm
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Semaphore

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
        self.db = PostgresDB("BuildingData","Mads", os.environ['DB_PASSWORD'])
        self.fetch_adress_data()
        self.bbr_data = None
        self.semaphore = Semaphore(10)  # Limit the number of concurrent threads to 100

        #Temporary fix to avoid duplicates
        #self.db.connect()
        #self.ids_in_db = self.db.fetch_data("SELECT adgangs_adresse_id FROM public.buildings;", as_df=True)['adgangs_adresse_id'].to_list()

    def fetch_adress_data(self) -> None:
       # if f'Adress_data_{self.municipality_id}.csv' not in os.listdir('Data/Adress_data'):
        url = f'https://api.dataforsyningen.dk/adgangsadresser?kommunekode={self.municipality_id}&format=csv'
        dawa_data = pd.read_csv(url) # Fetch the data and save it to a csv file
        dawa_data.to_csv(self.adress_csv_path, index=False)
        
        #Figure out how many of the id's exist in the db already and remove the rows that does
        self.db.connect()
        self.ids_in_db = self.db.fetch_data("SELECT adgangs_adresse_id FROM public.buildings;", as_df=True)['adgangs_adresse_id'].to_list()
        dawa_data = dawa_data[~dawa_data['id'].isin(self.ids_in_db)]
        
        #reverse the order
        dawa_data.to_csv(self.adress_csv_path, index=False)

    def get_bbr_data(self, adgangs_adresse_id: str) -> List[Building]:
        
        #Lookup the data from the BBR API
        try:
            bbr_data = lookup_bbr_data(adgangs_adresse_id)
        except Exception as e:
            write_error_log(f"Error getting BBR data: {e}")
            return []

        #Load the data into the pydantic model
        bbr_data = load_pydantic_model(bbr_data)

        if len(bbr_data) == 0:
            return bbr_data

        #Check if the status of the building is active
        bbr_data = [item for item in bbr_data if item.status == '6']

        return bbr_data
    
    def get_closest_school(self, lattitude: float, longitude: float) -> str:
        #Lookup the data from the csv file with schools gathered from the schools pipeline: 
        school = lookup_nearest_school(lattitude, longitude)
        return school

    def run_etl(self) -> None:
        self.db.connect()
        rows = list(load_adress_data(self.adress_csv_path))
        
        def process_row(row):
            with self.semaphore:  # Ensure no more than 100 threads access this block
                adgangs_adresse_id = row.id
                lattitude, longitude = row.vejpunkt_y, row.vejpunkt_x
                road_name = row.adresseringsvejnavn
                house_number = row.husnr
                postal_code = row.postnr
                postal_code_name = row.postnrnavn

                # Get the BBR data for the given adgangs_adresse_id
                bbr_data = self.get_bbr_data(adgangs_adresse_id)
                if len(bbr_data) == 0:
                    return None

                # Get the closest school to the building
                closest_school = self.get_closest_school(lattitude, longitude)

                # Get the closest stations to the building
                metro_station = get_nearest_station(lattitude, longitude, 'metro')
                s_train_station = get_nearest_station(lattitude, longitude, 'train')
                bus_station = get_nearest_station(lattitude, longitude, 'bus')
                tram_station = get_nearest_station(lattitude, longitude, 'tram')

                # Write the data to the database
                self.write_to_database(
                    adgangs_adresse_id,
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
        
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(process_row, row) for row in rows]

            for idx, future in enumerate(tqdm(as_completed(futures), total=len(rows))):
                future.result()  # Raise exception if any occurred in threads

                # Optional: Sleep every 500 rows to manage API rate limiting
                if idx % 500 == 0:
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
                WITH road_name_inserted AS (
                    INSERT INTO road_name (road_name)
                    VALUES (%(road_name)s)
                    ON CONFLICT (road_name) DO NOTHING
                    RETURNING road_name_id
                )
                INSERT INTO "buildings" (
                    building_id,
                    construction_year,
                    ussage_code,
                    collected_area,
                    industry_area,
                    housing_area,
                    foot_print_area,
                    outer_wall_material_id,
                    roof_material_id,
                    water_supply_id,
                    drainage_id,
                    floors,
                    heating_source_id,
                    alternative_heating_id,
                    carport,
                    plot_id,
                    municipality_id,
                    longitude,
                    lattitude,
                    asbestos_code,
                    house_number,
                    road_name_id,
                    postal_code,
                    metro_id,
                    metro_distance,
                    s_train_id,
                    s_train_distance,
                    bus_id,
                    bus_distance,
                    tram_id,
                    tram_distance,
                    school_id,
                    school_distance,
                    adgangs_adresse_id,
                    updated_at
                ) VALUES ( 
                    %(building_id)s,
                    %(construction_year)s,
                    %(ussage_code)s,
                    %(collected_area)s,
                    %(industry_area)s,
                    %(housing_area)s,
                    %(foot_print_area)s,
                    %(outer_wall_material_id)s,
                    %(roof_material_id)s,
                    %(water_supply_id)s,
                    %(drainage_id)s,
                    %(floors)s,
                    %(heating_source_id)s,
                    %(alternative_heating_id)s,
                    %(carport)s,
                    %(plot_id)s,
                    %(municipality_id)s,
                    %(longitude)s,
                    %(lattitude)s,
                    %(asbestos_code)s,
                    %(house_number)s,
                    COALESCE(
                        (SELECT road_name_id FROM road_name_inserted),
                        (SELECT road_name_id FROM road_name WHERE road_name = %(road_name)s)
                    ),
                    %(postal_code)s,
                    %(metro_id)s,
                    %(metro_distance)s,
                    %(s_train_id)s,
                    %(s_train_distance)s,
                    %(bus_id)s,
                    %(bus_distance)s,
                    %(tram_id)s,
                    %(tram_distance)s,
                    %(school_id)s,
                    %(school_distance)s,
                    %(adgangs_adresse_id)s,
                    NOW()
                )
                """
            params = {
                "building_id": building.id_lokalId,
                "construction_year": building.byg026Opførelsesår,
                "ussage_code": building.byg021BygningensAnvendelse,
                "collected_area": building.byg038SamletBygningsareal,
                "housing_area": building.byg039BygningensSamledeBoligAreal,
                "foot_print_area": building.byg041BebyggetAreal,
                "industry_area": building.byg040BygningensSamledeErhvervsAreal,
                "outer_wall_material_id": building.byg032YdervæggensMateriale,
                "roof_material_id": building.byg033Tagdækningsmateriale,
                "water_supply_id": building.byg030Vandforsyning,
                "drainage_id": building.byg031Afløbsforhold,
                "floors": building.byg054AntalEtager,
                "heating_source_id": building.byg056Varmeinstallation,
                "alternative_heating_id": building.byg058SupplerendeVarme,
                "carport": building.byg043ArealIndByggetCarport,
                "plot_id": building.grund,
                "municipality_id": building.kommunekode,
                "asbestos_code": building.byg036AsbestholdigtMateriale,
                "longitude": longitude,
                "lattitude": lattitude,
                "house_number": house_number,
                "road_name": road_name,
                "postal_code": postal_code,
                "metro_id": metro_station.station_id,
                "metro_distance": metro_station.distance,
                "s_train_id": s_train_station.station_id,
                "s_train_distance": s_train_station.distance,
                "bus_id": bus_station.station_id,
                "bus_distance": bus_station.distance,
                "tram_id": tram_station.station_id,
                "tram_distance": tram_station.distance,
                "school_id": closest_school.school_id,
                "school_distance": closest_school.distance,
                "adgangs_adresse_id": adgangs_adresse_id
            }
            self.db.execute_query(insert_query, params)

        # Write to error log for the db log
        except Exception as e:
            self.db.write_error_log(f"Building ETL Failed with error: {e}")