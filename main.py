from utils.database import PostgresDB
from ETL_Scripts.bygnings_etl import BuildingETL

if __name__ == "__main__":
  etl = BuildingETL('0101')



# Example usage
#if __name__ == "__main__":
#    # Initialize the database connection
#    db = PostgresDB("BuildingData","Mads","Hv06f19!")
#
#    try:
#        db.connect()
#
#        # Example: Create a table
#        create_table_query = """
#        CREATE TABLE "Buildings" (
#          "Building_Id" int PRIMARY KEY NOT NULL,
#          "construction_year" int,
#          "ussage_code" int,
#          "collected_area" int,
#          "industry_area" int,
#          "foot_print_area" int,
#          "outer_wall_meterial" int,
#          "roof_material" int,
#          "floors" int,
#          "heating_source_id" int,
#          "shelter_space" int
#        );
#        """
#        db.execute_query(create_table_query)
#
#    finally:
#        db.close()