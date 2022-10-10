from email.policy import default
from .enums import MunicipalityTypes, Provinces
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models
from django.urls import reverse
from django.contrib.gis.geos import Point
import json


class WardManager(models.Manager):

    def closest(self, pt: Point):
        qs = self.get_queryset()
        ward_and_distance = []
        for ward in qs:
            ward_pt = Point((ward.map_longitude, ward.map_latitude))
            ward_and_distance.append((ward, pt.distance(ward_pt)*100))

        ward_and_distance = sorted(ward_and_distance, key=lambda x: x[1])

        return ward_and_distance[0][0]


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
    area_number = models.IntegerField(null=True)
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

    def toDict(self):
        """
        Returns a Dict version of the Municipality
        """
        return {
            "name": self.name, 
            "municipality_code": self.municipality_code, 
            "municipality_type": self.municipality_type, 
            "area_number": self.area_number, 
            "province": self.province
            }

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
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    boundary = models.MultiPolygonField(_("Ward Boundary data"), null=True)
    objects = WardManager()

    def __str__(self):
        return self.name

    @property
    def map_longitude(self):
        return self.boundary.centroid.coords[0]

    @property
    def map_latitude(self):
        return self.boundary.centroid.coords[1]

    @property
    def map_geoJson(self):
        return self.boundary.geojson

    def get_absolute_url(self):
        return reverse("ward_detail", kwargs={"municipality_code": self.municipality.municipality_code, "slug": self.slug})

    def toDict(self):
        """
        Returns a Dict version of the ward
        """
        return {
            "name": self.name, 
            "slug": self.slug, 
            "municipality":self.municipality.toDict(),
            "map_geoJson": self.map_geoJson
            
            }

    def toJsonUrl(self) -> str:
        """
        Converts a normal url, which may contain a trailing slash to a valid .json url
        """
        url = self.get_absolute_url()
        if url[-1] == "/":
            return url[:len(url)-1]+".json"
        return url + ".json"


class WardDetail(BaseModel):
    STAGING = "staging"
    PRODUCTION = "production"
    VERSION_CHOICES = [
        (STAGING, _("Staging version")),
        (PRODUCTION, _("Production version"))]

    STRING = "string"
    INT = "int"
    FLOAT = "float"
    DATE = "date"
    EMAIL = "email"
    PHONE = "phone"
    JSON = "json"
    FIELD_TYPES_CHOICES = [
        (STRING, _("String")),
        (INT, _("Integer")),
        (FLOAT, _("Float")),
        (JSON, _("Json")),
        (DATE, _("Date")),
        (EMAIL, _("Email")),
        (PHONE, _("Phone")),
    ]
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=90, null=False, blank=False)
    field_type = models.CharField(
        max_length=40, default=STRING, choices=FIELD_TYPES_CHOICES)
    field_value = models.CharField(max_length=90, null=False, blank=False)
    stage = models.CharField(
        max_length=40, default=STAGING, choices=VERSION_CHOICES)
    feedback = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.field_name} - {self.stage} - {self.ward}"
