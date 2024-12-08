import pandas as pd
from utils.database import PostgresDB
import os 
from pydantic import BaseModel, Field
from typing import List

class PostalArea(BaseModel):
    postal_code: int = Field(..., example=1000)
    postal_name: str = Field(..., example="København K")

def prepare_postal_area_table() -> List[PostalArea]:
    """
    Prepare the postal_area table by reading the data from the csv file and returning it as a pandas DataFrame.
    Download the overview from:
    https://view.officeapps.live.com/op/view.aspx?src=https://www.postnord.dk/siteassets/pdf/postnumre/regionsopdelt-postnummer-excel.xls
    """
    postal_areas = pd.read_excel("Data/postal_codes.xlsx", header=1)
    postal_areas = postal_areas.rename(columns={"POSTNR": "postal_code",
                                                "BYNAVN": "postal_name"})
    
    # Drop duplicates to avoid inserting the same data multiple times
    postal_areas = postal_areas.drop_duplicates(subset="postal_code", keep="first")

    # Create a list of PostalArea objects
    postal_areas = [PostalArea(**row.to_dict()) for _, row in postal_areas.iterrows()]
    return postal_areas


def populate_postal_area() -> None:
    """
    Populate the postal_area table in the database with data from the csv file.
    """
    # Prepare the data
    postal_areas = prepare_postal_area_table()

    # Initialize the database connection
    db = PostgresDB("BuildingData", "Mads", os.environ['DB_PASSWORD'])
    try:
        # Connect to the database
        db.connect()

        # Insert the data into the database
        for postal_area in postal_areas:
            query = """
            INSERT INTO postal_area (postal_code, postal_name)
            VALUES (%s, %s);
            """
            params = (postal_area.postal_code, postal_area.postal_name)
            db.execute_query(query, params)

    finally:
        db.close()