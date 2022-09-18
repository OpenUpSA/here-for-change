from django.contrib.auth.models import User
from .enums import MunicipalityTypes, Provinces
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiPolygon,Point



class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Municipality(BaseModel):
    name = models.CharField(max_length=255, unique=True,
                            blank=False, null=False)
    municipality_code = models.CharField(
        max_length=6, unique=True, blank=False, null=False)
    municipality_type = models.CharField(
        max_length=25, choices=MunicipalityTypes.choices, null=False, blank=False
    )
    area_number=models.IntegerField(null=True)
    province = models.CharField(
        max_length=25, choices=Provinces.choices, null=False, blank=False
    )
    district = models.CharField(max_length=255, null=True, blank=True)

    map_default_zoom = models.IntegerField(default=12, null=False, blank=False)
    map_latitude = models.DecimalField(
        default=-33.9249, max_digits=10, decimal_places=7, null=False, blank=False)
    map_longitude = models.DecimalField(
        default=18.4241, max_digits=10, decimal_places=7, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Municipalities"

    def __str__(self):
        return self.name


def ward_slug(instance):
    return instance.municipality.municipality_code + ' ' + instance.name


class Ward(BaseModel):
    name = models.CharField(max_length=255, unique=False,
                            blank=False, null=False)
    slug = AutoSlugField(populate_from=ward_slug)
    municipality = models.ForeignKey(
        Municipality, on_delete=models.CASCADE, null=False, blank=False
    )
    map_default_zoom = models.IntegerField(default=12, null=False, blank=False)
    map_latitude = models.DecimalField(
        default=-33.9249, max_digits=10, decimal_places=7, null=False, blank=False)
    map_longitude = models.DecimalField(
        default=18.4241, max_digits=10, decimal_places=7, null=False, blank=False)
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    boundary = models.MultiPolygonField(_("Ward Boundary data"),null=True)

    def __str__(self):
        return self.name
    @property
    def longitude(self):
        
        return self.boundary.centroid.coords[0]
    @property
    def latitude(self):
        return self.boundary.centroid.coords[1]

    @property
    def map_geoJson(self):
        return self.boundary.geojson
