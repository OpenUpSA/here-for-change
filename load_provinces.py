"""
Fetches Provinces from mapit and saves to db
"""
from django.contrib.gis.geos import MultiPolygon,Polygon
import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'here_for_change.settings')
django.setup()

from here_for_change.municipalities.models import Province

SOURCE_URL="https://mapit.openup.org.za/area/"
SOUTH_AFRICA_AREA_CODE="4577"

def load_provinces():
    """
    Fetches South Africa area children (Provinces) from mapit and saves them to db
    """
    res=requests.get(f"{SOURCE_URL}{SOUTH_AFRICA_AREA_CODE}/children.json")
    children=json.loads(res.content)
    provinces=list(dict.fromkeys(list(children.keys())))
    for area_number in provinces:
        province=children[area_number]
        try:
            province_object=Province(name=province["name"],area_number=province["id"],province_code=province["codes"]["MDB"])
            province_object.save()
        except Exception as e:
            raise e

if __name__=="__main__":
    load_provinces()









