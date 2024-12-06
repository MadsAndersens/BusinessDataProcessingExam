import requests
import pandas as pd
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import json 
import os

class Etage(BaseModel):
    id_lokalId: str
    etage: dict = Field(alias='etage')

class Opgang(BaseModel):
    id_lokalId: str
    opgang: dict = Field(alias='opgang')

class BuildingData(BaseModel):
    datafordelerOpdateringstid: datetime
    byg007Bygningsnummer: int = None
    byg021BygningensAnvendelse: str = None
    byg026Opførelsesår: int = None
    byg041BebyggetAreal: Optional[int] = None
    byg038SamletBygningsareal: Optional[int] = None
    byg039BygningensSamledeBoligAreal: Optional[int] = None
    
    class Config:
        allow_population_by_field_name = True

# Usage example
def parse_building_data(data: List[dict]) -> List[BuildingData]:
    return [BuildingData.model_validate(item) for item in data]


def lookup_dawa_adress(address: str) -> dict:
    # Trin 1: Brug DAWA's API til at finde adgangsadresse-ID'et
    dawa_url = "https://api.dataforsyningen.dk/adresser"
    params = {"q": address}
    response = requests.get(dawa_url, params=params)
    response.raise_for_status()
    addresses = response.json()
    return addresses


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
    
def get_bbr_data(address: str) -> List[BuildingData]:
    addresses = lookup_dawa_adress(address)

    if not addresses:
        return None

    # Antag, at det første resultat er det korrekte
    adgangsadresse_id = addresses[0]["adgangsadresse"]["id"]

    #Get the BBR Data
    response = lookup_bbr_data(adgangsadresse_id)
    
    # Håndter fejlstatusser
    if response.status_code == 400:
        raise ValueError("Bad Request: Kontroller adgangsadresse-ID og forespørgslens struktur.")
    elif response.status_code == 401:
        raise ValueError("Unauthorized: Kontroller dit brugernavn og adgangskode.")
    elif response.status_code != 200:
        raise ValueError(f"HTTP Error {response.status_code}: {response.text}")
    bbr_data = response.json()

    return parse_building_data(bbr_data)


