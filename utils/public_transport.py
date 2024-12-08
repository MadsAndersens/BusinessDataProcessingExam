import pandas as pd
from haversine import haversine, Unit
from pydantic import BaseModel, Field


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