import pandas as pd
import os
from haversine import haversine, Unit
from pydantic import BaseModel, Field

from utils.database import PostgresDB


#Define metro station data model
class Station(BaseModel):
    station_id: int
    station_name: str
    latitude: float 
    longitude: float
    distance: float = None


def get_nearest_station(lattitude: float,
                        longitude: float,
                        station_type: str) -> BaseModel:
    """
    Lookup the nearest station to the given lattitude and longitude and return the station as a pydantic model
    """
    #Load the stations data
    stations = pd.read_csv('Data/stations.csv')
    stations['latitude'] = stations['latitude'].str.replace(',','.').astype(float)
    stations['longitude'] = stations['longitude'].str.replace(',','.').astype(float)

    #Filter the stations based on the station type
    stations = stations[stations[station_type] == 1][["station_name","station_id","latitude","longitude"]]

    #Create a pydantic model for the stations
    stations = [Station(**station.to_dict()) for _,station in stations.iterrows()]
    
    #Find the closest station
    closest_station = None
    min_distance = float('inf')
    for station in stations:
        distance = haversine((lattitude, longitude), (station.latitude, station.longitude), unit=Unit.METERS)
        if distance < min_distance:
            min_distance = distance
            closest_station = station
    
    #Set the distance to the closest station
    closest_station.distance = min_distance

    return closest_station

def populate_station_data() -> None:
    """
    Populate the station tables in the database with data from the csv file.
    """
    # Initialize the database connection
    db = PostgresDB("BuildingData", "Mads", os.environ['DB_PASSWORD'])
    try:
        # Connect to the database
        db.connect()

        # Read the data from the csv file
        stations = pd.read_csv("Data/stations.csv")
        stations['latitude'] = stations['latitude'].str.replace(',', '.').astype(float)
        stations['longitude'] = stations['longitude'].str.replace(',', '.').astype(float)

        for idx, row in stations.iterrows():
            station_id = row['station_id']
            station_name = row['station_name']
            latitude = row['latitude']
            longitude = row['longitude']
            metro = row['metro']
            train = row['train']
            bus = row['bus']
            tram = row['tram']

            # Insert the station data into the database
            if metro == 1:
                db.execute_query("""
                    INSERT INTO metro (metro_id, metro_name, latitude, longitude)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (metro_id) DO NOTHING
                """, (station_id, station_name, latitude, longitude))

            if train == 1:
                db.execute_query("""
                    INSERT INTO s_train (s_train_id, s_train_name, latitude, longitude)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (s_train_id) DO NOTHING
                """, (station_id, station_name, latitude, longitude))

            if bus == 1:
                db.execute_query("""
                    INSERT INTO bus (bus_id, bus_name, latitude, longitude)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (bus_id) DO NOTHING
                """, (station_id, station_name, latitude, longitude))

            if tram == 1:
                db.execute_query("""
                    INSERT INTO tram (tram_id, tram_name, latitude, longitude)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (tram_id) DO NOTHING
                """, (station_id, station_name, latitude, longitude))
    finally:
        db.close()