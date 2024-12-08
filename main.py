from utils.database import PostgresDB, init_db
from ETL_Scripts.bygnings_etl import BuildingETL
import os

if __name__ == "__main__":
  #init_db()
  etl = BuildingETL('0101')
  etl.run_etl()
