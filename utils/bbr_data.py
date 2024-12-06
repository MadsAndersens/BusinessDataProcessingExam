import requests
import pandas as pd
from typing import List, Optional
from pydantic import BaseModel, Field, TypeAdapter
from datetime import datetime
import json 
import os

class Building(BaseModel):
    datafordelerOpdateringstid: datetime
    byg021BygningensAnvendelse: str
    byg026Opførelsesår: int
    byg030Vandforsyning: str
    byg031Afløbsforhold: str
    byg032YdervæggensMateriale: str
    byg033Tagdækningsmateriale: str
    byg037KildeTilBygningensMaterialer: str
    byg038SamletBygningsareal: int
    byg039BygningensSamledeBoligAreal: int
    byg040BygningensSamledeErhvervsAreal: int
    byg041BebyggetAreal: int
    byg053BygningsarealerKilde: str
    byg054AntalEtager: int
    byg056Varmeinstallation: str
    byg058SupplerendeVarme: str
    byg094Revisionsdato: datetime
    byg133KildeTilKoordinatsæt: str
    byg134KvalitetAfKoordinatsæt: str
    byg135SupplerendeOplysningOmKoordinatsæt: str
    byg136PlaceringPåSøterritorie: str
    byg404Koordinat: str
    byg406Koordinatsystem: str
    forretningshændelse: str
    forretningsområde: str
    grund: str
    husnummer: str
    id_lokalId: str
    jordstykke: str
    kommunekode: str
    status: str
    byg036AsbestholdigtMateriale: str = '5'
    byg043ArealIndByggetCarport: int = 0

# Since the buildings are returned as a list for that specific entrance point ID
def validate_json_data(response) -> None:
    # Create a type adapter for the list of buildings
    person_list_adapter = TypeAdapter(list[Building]) 
    
    # Now validate the reponse as a string representation of the JSON data
    response_str = json.dumps(response.json(),ensure_ascii=False)
    print(response_str)
    person_list_adapter.validate_json(response_str)

def load_pydantic_model(response: requests.Response) -> List[Building]:
    
    #Validate the data
    try:
        validate_json_data(response)
    except Exception as e:
        raise ValueError(f"Data did not fit model {e}")
    
    #Unpack the data into the pydantic model: 
    data = [Building(**item) for item in response.json()]

    return data
    

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
    return response
