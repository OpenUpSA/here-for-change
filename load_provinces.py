"""
Fetches Provinces from mapit and saves to db
"""
import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'here_for_change.settings')
django.setup()

from here_for_change.municipalities.models import Province
from django.contrib.gis.geos import MultiPolygon,Polygon

SOURCE_URL="https://mapit.openup.org.za/"
SOUTH_AFRICA_AREA_CODE="4577"

def load_provinces():
    """
    Fetches South Africa area children (Provinces) from mapit and saves them to db
    """
    res=requests.get(f"{SOURCE_URL}area/{SOUTH_AFRICA_AREA_CODE}/children.json")
    children=json.loads(res.content)
    provinces=list(dict.fromkeys(list(children.keys())))
    boundaries=get_boundaries(provinces)
    for area_number in provinces:
        province=children[area_number]
        try:
            province_object=Province(name=province["name"],area_number=province["id"],province_code=province["codes"]["MDB"])
            province_object=load_boundary_in_province(boundaries,province_object,int(area_number))
            province_object.save()
        except Exception as e:
            raise e

def get_boundaries(area_numbers:list)->list:
    """
    Fetches all boundaries of items in area_numbers list
    """
    res=requests.get(f"{SOURCE_URL}areas/{','.join(area_numbers)}.geojson")
    data=json.loads(res.content)    
    return data["features"]


def load_boundary_in_province(boundaries:list,province:Province,area_number:int)->Province:
    """Load new boundary in Province
    :param list boundaries: List of boundaries which may contain ward boundary
    :param Province province: Province object new boundaries will be loaded into
    :param int area_number: area number of Province instance boundaries are being loaded in
    :rtype:Province
    """

    for boundary in boundaries: 
        if area_number == int(boundary["properties"]["id"]):
            print(f"{province.name} - {area_number}")
            if boundary["geometry"]["type"]=="MultiPolygon":
                province_boundary=MultiPolygon()
                for shape in boundary["geometry"]["coordinates"]:
                    province_boundary=province_boundary.union(MultiPolygon([ Polygon(polygon) for polygon in shape]))
                province.boundary=province_boundary
            else:
                province.boundary=MultiPolygon([ Polygon(polygon) for polygon in boundary["geometry"]["coordinates"]])
            break
    return province

if __name__=="__main__":
    Province.objects.all().delete()
    load_provinces()









