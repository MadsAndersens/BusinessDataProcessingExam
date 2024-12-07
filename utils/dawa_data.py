from pydantic import BaseModel, Field, TypeAdapter
import csv

class BuildingAdress(BaseModel):
    id: str
    husnr: str
    adresseringsvejnavn: str
    postnr: int
    postnrnavn: str
    vejpunkt_x: float
    vejpunkt_y: float

def load_adress_data(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield BuildingAdress(**row)

