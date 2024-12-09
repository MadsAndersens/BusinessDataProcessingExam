import requests
import pandas as pd
from typing import List, Optional
from pydantic import BaseModel, Field, TypeAdapter
from datetime import datetime
import json 
import os
import time

class Building(BaseModel):
    id_lokalId: str
    datafordelerOpdateringstid: datetime
    grund: str 
    kommunekode: str
    status: str
    husnummer: str
    byg021BygningensAnvendelse: str = None
    byg026Opførelsesår: int = None
    byg030Vandforsyning: str = None
    byg031Afløbsforhold: str = None
    byg032YdervæggensMateriale: str = None
    byg033Tagdækningsmateriale: str = None
    byg037KildeTilBygningensMaterialer: str = None
    byg038SamletBygningsareal: int = 0
    byg039BygningensSamledeBoligAreal: int  = 0
    byg040BygningensSamledeErhvervsAreal: int = 0
    byg041BebyggetAreal: int = 0
    byg054AntalEtager: int = 1
    byg056Varmeinstallation: str = None
    byg058SupplerendeVarme: str = None
    byg036AsbestholdigtMateriale: int = 5
    byg043ArealIndByggetCarport: int = 0

# Since the buildings are returned as a list for that specific entrance point ID
def validate_json_data(response) -> None:
    # Create a type adapter for the list of buildings
    person_list_adapter = TypeAdapter(list[Building]) 
    
    # Now validate the reponse as a string representation of the JSON data
    response_str = json.dumps(response.json(),ensure_ascii=False)
    person_list_adapter.validate_json(response_str)

def load_pydantic_model(response: requests.Response) -> List[Building]:
    
    #Validate the data
    try:
        validate_json_data(response)
    except Exception as e:
        write_error_log(f"Error validating JSON data: {e}")
        return []
    
    #Unpack the data into the pydantic model: 
    data = [Building(**item) for item in response.json()]

    return data

def write_error_log(error_message: str)-> None:
    """
    Write an error message to the error log file.

    :param error_message: Error message to write to the log file
    """
    with open("error_logs/bbr_log.txt", "a") as file:
        file.write(error_message + "\n")


# Usage example
def parse_building_data(data: List[dict]) -> List[Building]:
    return [Building.model_validate(item) for item in data]


def lookup_bbr_data(adgangsadresse_id: str) -> requests.Response:
    username = os.environ['DF_USERNAME']
    password = os.environ['DF_PASSWORD'] #st.session_state['MASTER_KEY']
    
    # Trin 2: Brug Datafordelerens BBR REST-tjeneste til at hente bygningens oplysninger
    bbr_url = "https://services.datafordeler.dk/BBR/BBRPublic/1/rest/bygning"
    params = {
        'username': username,
        'password': password,
        "husnummer": adgangsadresse_id
    }

    # Brug HTTP Basic Authentication til at sende brugernavn og adgangskode
    response = requests.get(bbr_url, params=params)

    # Check if the request was successful
    if response.status_code != 200:
        #Wait for 5 seconds and try again
        time.sleep(5)
        response = requests.get(bbr_url, params=params)
        if response.status_code != 200:
            raise ValueError(f"Failed to get data from BBR API. Status code: {response.status_code}")
    
    return response
