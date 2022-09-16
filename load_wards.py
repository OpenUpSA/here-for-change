"""
This script is responsible for fetching wards and loading the data in Model
"""

import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'here_for_change.settings')
django.setup()

from here_for_change.municipalities.models import Ward
from here_for_change.municipalities.models import Municipality

SOURCE_URL="https://mapit.openup.org.za/area/"

def get_municipality_children(muni_area_number:int):
    """Get wards in municipality
    :param int muni_area_number: Area number of municipality to get children of
    :rtype: dict{int:dict}
    """
    data=requests.get(f"{SOURCE_URL}/{muni_area_number}/children")
    print(data.content)


def load_boundary_in_ward(area_number:int,ward:Ward):
    """Load new boundary in ward
    :param int area_number: Area number used to fetch Ward boundary
    :param Ward ward: Ward object new boundaries will be loaded into
    :rtype:None
    """
    ...

if __name__=="__main__":
    for municipality in Municipality.objects.all():

        if municipality.area_number:
            get_municipality_children(municipality.area_number)
            print("in")









