import pandas as pd
from haversine import haversine, Unit
from pydantic import BaseModel, Field


#Define metro station data model
class MetroStation(BaseModel):
    station_id: str = Field(alias='id')
    station_name: str = Field(alias='navn')
    lattitude: float = Field(alias='koordinater')
    longitude: float = Field(alias='koordinater')
    distance: float = None

#Define s-train station data model
class STrainStation(BaseModel):
    station_id: str = Field(alias='id')
    station_name: str = Field(alias='navn')
    lattitude: float = Field(alias='koordinater')
    longitude: float = Field(alias='koordinater')
    distance: float = None

#Define bus station data model
class BusStation(BaseModel):
    station_id: str = Field(alias='id')
    station_name: str = Field(alias='navn')
    lattitude: float = Field(alias='koordinater')
    longitude: float = Field(alias='koordinater')
    distance: float = None

#Define tram station data model
class TramStation(BaseModel):
    station_id: str = Field(alias='id')
    station_name: str = Field(alias='navn')
    lattitude: float = Field(alias='koordinater')
    longitude: float = Field(alias='koordinater')
    distance: float = None


def get_nearest_station(lattitude: float,
                        longitude: float,
                        station_type: str) -> BaseModel:
    """
    Lookup the nearest station to the given lattitude and longitude and return the station as a pydantic model
    """
    #Load the stations data
    stations = pd.read_csv('Data/stations.csv')
    stations = stations[stations[station_type] == 1][["station_name","station_id","latitude","longitude"]]

    #Create a pydantic model for the stations
    stations = stations.apply(lambda row: MetroStation(**row.to_dict()), axis=1)
    
    #Find the closest station
    closest_station = None
    min_distance = float('inf')
    for station in stations:
        distance = haversine((lattitude, longitude), (station.lattitude, station.longitude), unit=Unit.METERS)
        if distance < min_distance:
            min_distance = distance
            closest_station = station

    return closest_station