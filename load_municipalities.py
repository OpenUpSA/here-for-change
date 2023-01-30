"""
Fetches Municipalities from mapit and saves to db
"""
import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'here_for_change.settings')
django.setup()

from here_for_change.municipalities.models import (Province,Municipality)
from here_for_change.municipalities.enums import MunicipalityTypes
from django.contrib.gis.geos import MultiPolygon,Polygon, GEOSGeometry


SOURCE_URL="https://mapit.openup.org.za/"

def create_municipality(name:str,area_number:int,municipality_code:str,province:Province,boundaries:list,district:str=None):
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
        municipality_object=load_boundary_in_municipality(boundaries,municipality_object,area_number)
        municipality_object.save()
    except Exception as e:
        raise e


def load_children(parent_area_code:int,province:Province,district:str=None):
    """
    Fetches and saves children of provinces and districts and municipality
    """
    res=requests.get(f"{SOURCE_URL}area/{parent_area_code}/children.json")
    children_dict=json.loads(res.content)
    children=list(dict.fromkeys(list(children_dict.keys())))
    boundaries=get_boundaries(children)
    for area_number in children:     
        child=children_dict[area_number]
        if child["type_name"]=="District":
            load_children(int(child["id"]), province, child["name"])
        else:
            create_municipality(child["name"],int(child["id"]),child["codes"]["MDB"],province,boundaries,district)

def load_municipalities():
    Municipality.objects.all().delete()
    for province in Province.objects.all().order_by("name"):
        load_children(province.area_number,province)

def get_boundaries(area_numbers:list)->list:
    """
    Fetches all boundaries of items in area_numbers list
    """
    res=requests.get(f"{SOURCE_URL}areas/{','.join(area_numbers)}.geojson")
    data=json.loads(res.content)    
    return data["features"]


def load_boundary_in_municipality(boundaries:list,municipality:Municipality,area_number:int)->Municipality:
    """Load new boundary in Municipality
    :param list boundaries: List of boundaries which may contain ward boundary
    :param Municipality municipality: Municipality object new boundaries will be loaded into
    :param int area_number: area number of Municipality instance boundaries are being loaded in
    :rtype:Municipality
    """

    for boundary in boundaries: 
        if area_number == int(boundary["properties"]["id"]):
            print(f"{municipality.name} - {area_number}")
            geom=GEOSGeometry(str(boundary["geometry"])).simplify(tolerance=0.01)
            if geom.__class__==Polygon:
                geom=MultiPolygon([geom])
            municipality.boundary=geom
            break
    return municipality

if __name__=="__main__":
    load_municipalities()










