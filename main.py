from utils.database import PostgresDB, create_building_table
from ETL_Scripts.bygnings_etl import BuildingETL
import os

if __name__ == "__main__":
  create_building_table()
  etl = BuildingETL('0101')
  etl.run_etl()
