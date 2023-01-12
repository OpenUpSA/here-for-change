"""
This script is calculates and saves Municipality boundaries
"""
from django.contrib.gis.geos import MultiPolygon, Polygon
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'here_for_change.settings')
django.setup()

from here_for_change.municipalities.models import (Ward,Municipality)

def get_municipality_boundary(municipality:Municipality)->MultiPolygon:
    """
    Returns the combined boundary of all wards in the municipality
    """
    wards=Ward.objects.filter(municipality=municipality)
    total_boundary=MultiPolygon()
    for ward in wards:        
        total_boundary=total_boundary.union(ward.boundary)
    if type(total_boundary)==Polygon:
        total_boundary=MultiPolygon([total_boundary])
    return total_boundary


if __name__=="__main__":
    for municipality in Municipality.objects.all():
        municipality.boundary=get_municipality_boundary(municipality)
        municipality.save()









