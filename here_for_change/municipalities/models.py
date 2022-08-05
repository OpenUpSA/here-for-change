from django.db import models
from django.contrib.auth.models import User
from .enums import MunicipalityTypes, Provinces
from autoslug import AutoSlugField


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
    province = models.CharField(
        max_length=25, choices=Provinces.choices, null=False, blank=False
    )

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

    def __str__(self):
        return self.name
