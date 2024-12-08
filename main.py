from utils.database import PostgresDB, init_db
from ETL_Scripts.bygnings_etl import BuildingETL
from utils.public_transport import populate_station_data
from utils.school_utils import populate_school_dimension
import os

from sql_inserts.postal_code_insert import populate_postal_area

if __name__ == "__main__":
  #init_db()
  etl = BuildingETL('0101')
  etl.run_etl()
