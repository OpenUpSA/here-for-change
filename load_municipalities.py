"""
Fetches Municipalities from mapit and saves to db
"""
from django.contrib.gis.geos import MultiPolygon,Polygon
import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'here_for_change.settings')
django.setup()

from here_for_change.municipalities.models import (Province,Municipality)
from here_for_change.municipalities.enums import MunicipalityTypes

SOURCE_URL="https://mapit.openup.org.za/area/"

def create_municipality(name:str,area_number:int,municipality_code:str,province:Province,district:str=None):
    """
    Creates and saves a municipality
    """
    try:
        municipality_object=Municipality(name=name,area_number=area_number,municipality_code=municipality_code,province=province)
        if district:
            municipality_object.district=district
            municipality_object.municipality_type=MunicipalityTypes.LOCAL
        else:
            municipality_object.municipality_type=MunicipalityTypes.METRO
        municipality_object.save()
    except Exception as e:
        raise e


def load_children(parent_area_code:int,province:Province,district:str=None):
    """
    Fetches and saves children of provinces and districts and municipality
    """
    res=requests.get(f"{SOURCE_URL}{parent_area_code}/children.json")
    children_dict=json.loads(res.content)
    children=list(dict.fromkeys(list(children_dict.keys())))
    
    for area_number in children:     
        child=children_dict[area_number]
        if child["type_name"]=="District":
            load_children(int(child["id"]), province, child["name"])
        else:
            create_municipality(child["name"],int(child["id"]),child["codes"]["MDB"],province,district)

def load_municipalities():
    Municipality.objects.all().delete()
    for province in Province.objects.all().order_by("name"):
        load_children(province.area_number,province)

if __name__=="__main__":
    load_municipalities()










