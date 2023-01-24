from .enums import MunicipalityTypes
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models
from django.urls import reverse
from django.contrib.gis.geos import Point

def default_feedback():
    return {"positive":0,"negative":0}

class MunicipalityManager(models.Manager):

    def closest(self, pt: Point):
        qs = self.get_queryset()
        municipality_and_distance = []
        for municipality in qs:
            municipality_pt=Point((municipality.map_latitude,municipality.map_longitude))
            municipality_and_distance.append((municipality, pt.distance(municipality_pt)*100))

        municipality_and_distance = sorted(municipality_and_distance, key=lambda x: x[1])
        try:
            municipality=municipality_and_distance[0][0]
        except IndexError:
            municipality=Municipality()

        return municipality
    
    def closest_n(self, pt: Point, municipality,number:int):
        qs = self.get_queryset()
        if municipality:
            qs.exclude(pk=municipality.pk)
        municipality_and_distance = []
        for municipality in qs:
            municipality_pt=Point((municipality.map_latitude,municipality.map_longitude))
            municipality_and_distance.append((municipality, pt.distance(municipality_pt)*100))

        municipality_and_distance = sorted(municipality_and_distance, key=lambda x: x[1])
        try:
            municipalities= [municipality_distance[0] for municipality_distance in municipality_and_distance][:number]
        except IndexError:
            municipalities=[municipality_distance[0] for municipality_distance in municipality_and_distance]

        return municipalities

class WardManager(models.Manager):

    def closest(self, pt: Point, ward=None):
        qs = self.get_queryset()
        if ward:
            qs.exclude(pk=ward.pk)
        ward_and_distance = []
        for ward in qs:
            ward_pt = Point((ward.map_latitude, ward.map_longitude))
            ward_and_distance.append((ward, pt.distance(ward_pt)*100))

        ward_and_distance = sorted(ward_and_distance, key=lambda x: x[1])
        try:
            ward=ward_and_distance[0][0]
        except IndexError:
            ward=Ward()

        return ward


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Province(BaseModel):
    name = models.CharField(max_length=255, unique=True,
                            blank=False, null=False)
    province_code = models.CharField(
        max_length=6, unique=True, blank=False, null=False)
    area_number = models.IntegerField(null=True)
    map_default_zoom = models.IntegerField(default=12, null=False, blank=False)

    boundary = models.MultiPolygonField(_("Province Boundary data"), null=True)

    @property
    def map_longitude(self):
        return self.boundary.centroid.coords[0]

    @property
    def map_latitude(self):
        return self.boundary.centroid.coords[1]

    @property
    def map_geoJson(self):
        return self.boundary.geojson

    class Meta:
        verbose_name_plural = "Provinces"

    def toDict(self,include_children:bool=False,include_boundary:bool=True, include_children_boundary:bool=False)->dict:
        """
        Returns a Dict object of the Province
        :param bool include_children: Specifies if the json object of this instance returned should include children.
        :param bool include_boundary: Specifies if the json object of this instance returned should include boundary data.
        :param bool include_children_boundary: Specifies if the json object of this instance returned should include children boundary data.
        """
        data = {
            "name": self.name, 
            "province_code": self.province_code, 
            "area_number": self.area_number, 
            }
        if include_boundary:
            data.update({"map_geoJson": self.map_geoJson})

        if include_children:
            data.update({"children": [municipality.toDict(include_boundary=include_children_boundary,include_children_boundary=include_children_boundary) for municipality in self.get_contained_municipalities()]})
        
        return data
    
    def get_contained_municipalities(self):
        return Municipality.objects.filter(province=self)

    def __str__(self):
        return self.name




class Municipality(BaseModel):
    name = models.CharField(max_length=255,blank=False, null=False)
    municipality_code = models.CharField(
        max_length=6, unique=True, blank=False, null=False)
    municipality_type = models.CharField(
        max_length=25, choices=MunicipalityTypes.choices, null=False, blank=False
    )
    area_number = models.IntegerField(null=True)
    province =models.ForeignKey(
        Province, on_delete=models.CASCADE, null=False, blank=False
    )
    district = models.CharField(max_length=255, null=True, blank=True)
    map_default_zoom = models.IntegerField(default=12, null=False, blank=False)

    boundary = models.MultiPolygonField(_("Municipality Boundary data"), null=True)
    objects=MunicipalityManager()

    @property
    def map_longitude(self):
        return self.boundary.centroid.coords[0]

    @property
    def map_latitude(self):
        return self.boundary.centroid.coords[1]

    @property
    def map_geoJson(self):
        return self.boundary.geojson

    class Meta:
        verbose_name_plural = "Municipalities"

    def toDict(self,include_children:bool=True,include_boundary:bool=True, include_children_boundary:bool=True)->dict:
        """
        Returns a Dict version of the Municipality
        :param bool include_children: Specifies if the json object of this instance returned should include children.
        :param bool include_boundary: Specifies if the json object of this instance returned should include boundary data.
        :param bool include_children_boundary: Specifies if the json object of this instance returned should include children boundary data.
        """
        data= {
            "name": self.name, 
            "municipality_code": self.municipality_code, 
            "municipality_type": self.municipality_type, 
            "area_number": self.area_number, 
            "province": self.province.name,
            }
        if include_boundary:
            data.update({"map_geoJson": self.map_geoJson})

        if include_children:
            data.update({"children": [ward.toDict(include_boundary=include_children_boundary) for ward in self.get_contained_wards()]})
        
        return data
    
    def get_contained_wards(self):
        return Ward.objects.filter(municipality=self)

    def __str__(self):
        return self.name


def ward_slug(instance):
    return instance.municipality.municipality_code + ' ' + instance.name


class Ward(BaseModel):
    name = models.CharField(
        max_length=255,blank=False, null=False)
    slug = AutoSlugField(populate_from=ward_slug)
    municipality = models.ForeignKey(
        Municipality, on_delete=models.CASCADE, null=False, blank=False
    )
    map_default_zoom = models.IntegerField(default=12, null=False, blank=False)
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

    @property
    def formatted_name(self):
        return Ward.format_name(self.name)

    @property
    def coords(self):
        return [self.map_latitude,self.map_longitude]

    @staticmethod
    def format_name(name):
        splitted_names=name.split(" ")
        return f"{splitted_names[-2]} {splitted_names[-1]}"
        

    def get_absolute_url(self):
        return reverse("ward_detail", kwargs={"municipality_code": self.municipality.municipality_code, "slug": self.slug})

    def toDict(self,include_boundary:bool=True):
        """
        Returns a Dict version of the ward
        :param bool include_boundary: Specifies if the json object of this instance returned should include boundary data.
        """
        data = {
            "name": self.name, 
            "formatted_name":Ward.format_name(self.name),
            "slug": self.slug, 
            "municipality":self.municipality.name,
            "map_default_zoom": self.map_default_zoom,
            "absolute_url":self.get_absolute_url()
            
            }

        if include_boundary:
            data.update({"map_geoJson": self.map_geoJson})
        
        return data

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
    feedback = models.JSONField(null=False, blank=False,  default=default_feedback)

    def __str__(self):
        return f"{self.field_name} - {self.stage} - {self.ward}"
    


class MunicipalityDetail(BaseModel):
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
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=200, null=False, blank=False)
    field_type = models.CharField(
        max_length=40, default=STRING, choices=FIELD_TYPES_CHOICES)
    field_value = models.CharField(max_length=200, null=False, blank=False)
    stage = models.CharField(
        max_length=40, default=STAGING, choices=VERSION_CHOICES)
    feedback = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.field_name} - {self.stage} - {self.municipality}"


class FindMyWardCouncillorFeedback(BaseModel):
    email=models.EmailField(null=False,blank=False)
    feedback=models.CharField(null=False,blank=False, max_length=250)
    ward=models.ForeignKey(Ward,null=False,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ward} - {self.email}"

