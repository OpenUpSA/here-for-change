from django.db import models


class MunicipalityTypes(models.TextChoices):
    METRO = 'Metropolitan'
    LOCAL = 'Local'


class Provinces(models.TextChoices):
    EC = 'EasternCape', 'Eastern Cape'
    FS = 'Freestate', 'Free State'
    GP = 'Gauteng', 'Gauteng'
    KZN = 'KwaZuluNatal', 'KwaZulu-Natal'
    LP = 'Limpopo', 'Limpopo'
    MP = 'Mpumalanga', 'Mpumalanga'
    NC = 'NorthernCape', 'Northern Cape'
    NW = 'NorthWest', 'North West'
    WC = 'WesternCape', 'Western Cape'
