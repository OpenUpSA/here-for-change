"""
This script is responsible for fetching wards and loading the data in Model
"""
from django.contrib.gis.geos import MultiPolygon,Polygon,GEOSGeometry
import os
import django
import requests
import json
import time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'here_for_change.settings')
django.setup()

from here_for_change.municipalities.models import (Ward,Municipality,Province)
from threading import Thread


SOURCE_URL="https://mapit.openup.org.za/"

class LoadWardsInProvince(Thread):

    def __init__(self, province:Province):
        Thread.__init__(self)
        self.province = province

    def run(self):
        get_children_by_province(self.province)

def get_children_by_province(province:Province):
    print(f"Started : {province.name} \n")
    with requests.session() as session:
        for municipality in [municipality for municipality in Municipality.objects.filter(province=province)]:
            get_municipality_children(municipality,session)


def get_municipality_children(municipality:Municipality,session:requests.Session):
    """Get and stores wards in municipality
    :param int muni_area_number: Area number of municipality to get children of
    :rtype: None
    """
    res=session.get(f"{SOURCE_URL}area/{municipality.area_number}/children.json")
    children=json.loads(res.content)
    municipality_children=list(dict.fromkeys(list(children.keys())))
    
    boundaries=get_boundaries(municipality_children,session)
    for area_number in municipality_children:
        ward=children[area_number]
        try:
            ward_object=Ward(name=ward["name"],municipality=municipality,area_number=int(area_number))
            ward_object=load_boundary_in_ward(boundaries,ward_object,int(area_number))
            ward_object.save()
        except Exception as e:
            raise e
    print(f"Saved:{municipality.name}")

def get_boundaries(area_numbers:list,session:requests.Session)->list:
    """
    Fetches all boundaries of items in area_numbers list
    """
    res=session.get(f"{SOURCE_URL}areas/{','.join(area_numbers)}.geojson")
    data=json.loads(res.content)    
    return data["features"]


def load_boundary_in_ward(boundaries:list,ward:Ward,area_number:int)->Ward:
    """Load new boundary in ward
    :param list boundaries: List of boundaries which may contain ward boundary
    :param Ward ward: Ward object new boundaries will be loaded into
    :param int area_number: area number of ward instance boundaries are being loaded in
    :rtype:Ward
    """
    for boundary in boundaries: 
        if area_number == int(boundary["properties"]["id"]):
            geom=GEOSGeometry(str(boundary["geometry"])).simplify()
            if geom.__class__==Polygon:
                geom=MultiPolygon([geom])
            ward.boundary=geom
            break
    return ward



def load_wards():
    for province in [province for province in Province.objects.all()]:
        worker = LoadWardsInProvince(province)
        worker.start()


if __name__=="__main__":
    load_wards()









