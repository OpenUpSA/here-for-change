"""
This script is responsible for fetching wards and loading the data in Model
"""
from django.contrib.gis.geos import MultiPolygon,Polygon
import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'here_for_change.settings')
django.setup()

from here_for_change.municipalities.models import (Ward,Municipality)

SOURCE_URL="https://mapit.openup.org.za/area/"

def get_municipality_children(municipality):
    """Get wards in municipality
    :param int muni_area_number: Area number of municipality to get children of
    :rtype: dict{int:dict}
    """
    res=requests.get(f"{SOURCE_URL}{municipality.area_number}/children.json")
    children=json.loads(res.content)
    for area_number in children.keys():
        ward=children[area_number]
        try:
            ward_object=Ward(name=ward.get("name"),municipality=municipality)
            ward_object=load_boundary_in_ward(area_number,ward_object)
            ward_object.save()
        except:
            continue



def load_boundary_in_ward(area_number:int,ward:Ward)->Ward:
    """Load new boundary in ward
    :param int area_number: Area number used to fetch Ward boundary
    :param Ward ward: Ward object new boundaries will be loaded into
    :rtype:None
    """
    res=requests.get(f"{SOURCE_URL}{area_number}.geojson")
    data=json.loads(res.content)    
    ward.boundary=MultiPolygon([ Polygon(polygon) for polygon in data["coordinates"]])
    return ward

if __name__=="__main__":
    Ward.objects.all().delete()
    for municipality in Municipality.objects.all():
        if municipality.area_number:
            get_municipality_children(municipality)









