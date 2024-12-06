from utils.database import PostgresDB
from ETL_Scripts.bygnings_etl import BuildingETL
import os

if __name__ == "__main__":
  etl = BuildingETL('0101')
  etl.run_etl()



# Example usage
#if __name__ == "__main__":
#    # Initialize the database connection
#    db = PostgresDB("BuildingData","Mads",os.environ['DB_PASSWORD'])
#    try:
#        db.connect()
#
#        # Example: Create a table
#        create_table_query = """
#              CREATE TABLE "Buildings" (
#                "building_id" int PRIMARY KEY NOT NULL,
#                "construction_year" int,
#                "ussage_code" int,
#                "collected_area" int,
#                "industry_area" int,
#                "housing_area" int,
#                "foot_print_area" int,
#                "outer_wall_meterial" int,
#                "roof_material" int,
#                "water_supply" int,
#                "drainage" int,
#                "floors" int,
#                "heating_source_id" int,
#                "alternate_heating_source_id" int,
#                "carport" bool,
#                "plot_id" varchar,
#                "municipality_id" varchar,
#                "longitude" float,
#                "lattitude" float,
#                "asbestos_present" bool
#              );
#        """
#        db.execute_query(create_table_query)
#
#    finally:
#        db.close()