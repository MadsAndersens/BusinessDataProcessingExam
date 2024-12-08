from utils.database import PostgresDB, create_building_table, init_db
from ETL_Scripts.bygnings_etl import BuildingETL
import os

if __name__ == "__main__":
  init_db()
  #create_building_table()
  #etl = BuildingETL('0101')
  #etl.run_etl()
