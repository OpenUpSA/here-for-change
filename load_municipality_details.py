"""
Loads municipality details from data file into db
"""
import json
import django
import os
import googlemaps


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'here_for_change.settings')
django.setup()
from here_for_change.municipalities.models import (
    Municipality, MunicipalityDetail)
GMAP_API_KEY = "AIzaSyAcOEGhLjgM6DKeW0lTGZyJ_QqcLwO7GmA" # Should be secret


def geocode_address(address: str)->dict:
    """ Converts a text address to an approximate point location using googlemaps API """
    gmaps_key = googlemaps.Client(key=GMAP_API_KEY)
    approximate_location = gmaps_key.geocode(address)
    return approximate_location[0]["geometry"]["location"]


def slugify(string: str) -> str:
    """ Converts normal string to slug.\n Example: `Executive Mayor` -> `executive_mayor`. """
    return string.strip().lower().replace(" ", "_")


def deslugify(string: str) -> str:
    """ Converts slug to normal string.\n Example: `executive_mayor` -> `Executive Mayor`. """
    return string.replace("_", " ").capitalize()


def slugify_all_keys(data: dict) -> dict:
    """ Recursively slugifies all keys in dictionary and returns new dictionary with slugified keys. """
    new_data = {}
    for key in data.keys():
        new_key = slugify(key)
        new_data[new_key] = data[key]
        if type(new_data[new_key]) == dict:
            new_data[new_key] = slugify_all_keys(new_data[new_key])

    return new_data


def format_data(data: dict) -> dict:
    """
    Formats keys in data to ease parsing.
    Example: provinces become `Eastern Cape` -> `EasternCape`.\n
    Also slugifies all keys in municipality dict.
    """
    new_data = {}
    for province in data.keys():
        new_province = "".join(province.split(" "))
        new_data[new_province] = {}
        for municipality in data[province].keys():
            new_data[new_province][municipality] = slugify_all_keys(
                data[province][municipality])
    return new_data


def read_data() -> dict:
    """
    Read json data file
    """
    with open("municipality_details/data.json", "r") as fp:
        return json.loads(fp.read())


def save_data(data: dict):
    """
    Converts data to json and saves in file
    """
    with open("municipality_details/slugified-data.json", "w+") as fp:
        fp.write(json.dumps(data))
        fp.close()


def load_data(data: dict):
    """Loads data file into municipality details table."""
    for municipality in Municipality.objects.all():
        try:
            municipalty_information = data[municipality.province][municipality.name]
        except KeyError:
            print(
                f"{municipality.name} province or {municipality.name} municipality details not found in data file")
            continue
        load_municipality_details(municipality, municipalty_information)


def load_municipality_details(municipality: Municipality, data: dict):
    """Loads municipality details for specific municipality."""
    # load municipality data
    for info in data["municipality"].keys():

        field_value = data["municipality"][info]
        if type(field_value) == list:
            field_value = ", ".join(field_value)
        if info == "street_address":
            field_value={"address":field_value}
            field_value.update(geocode_address(data["municipality"][info]))
            field_value = json.dumps(field_value)
        municipality_detail, _ = MunicipalityDetail.objects.update_or_create(
            municipality=municipality, field_name=f"municipality_{info}", stage=MunicipalityDetail.PRODUCTION, defaults={"field_value": field_value, "field_type": "String"})

    # load name of municipality representative
    roles = ["executive_mayor", "mayor", "municipal_manager",
             "head_of_communications", "information_officer_(paia)"]
    for role in roles:
        try:
            municipality_information = data[role]
            municipality_detail, _ = MunicipalityDetail.objects.update_or_create(municipality=municipality, field_name=f"municipality_representative", stage=MunicipalityDetail.PRODUCTION, defaults={
                                                                                 "field_value": f"{municipality_information.get('name',' ')} ({deslugify(role)})", "field_type": "String"})
            break
        except KeyError:
            continue


if __name__ == "__main__":
    data = read_data()
    data = format_data(data)
    load_data(data)
