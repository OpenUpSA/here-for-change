"""
Load ward details into db from data file
"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'here_for_change.settings')
django.setup()

from here_for_change.municipalities.models import (Ward,Municipality,WardDetail)

DATA_FILE="./ward_details/data.json"

def load_data()->dict:
    data={}
    with open(DATA_FILE,"r") as fp:
        data=json.loads(fp.read())
        fp.close()
    return data

def format_municipality_names(data:dict)->dict:
    """
    Converts all municipality names from ABR - MUNICIPALITY_NAME to MUNICIPALITY_NAME removing "ABR - "
    """
    new_data={}
    for province in data.keys():
        new_data[province]={}
        for municipality in data[province].keys():
            formatted_municipality_name=" ".join(municipality.split(" ")[2:])
            new_data[province][formatted_municipality_name]=data[province][municipality]
    del data
    return new_data


def load_ward_details():
    """
    Loads ward details from json data file into database
    """
    data=load_data()
    data=format_municipality_names(data)
    for province in data.keys():
        print(f"\n{province}\n")
        municipalities=Municipality.objects.filter(province__name=province)
        for municipality in municipalities:
            try:
                municipality_data=data[province][municipality.name]
            except KeyError:
                print(f"Couldn't find Municipality: {municipality.name}")
                continue
            municipality_data_unique_keys=list(dict.fromkeys(list(municipality_data.keys())))
            for ward in municipality_data_unique_keys:

                ward_name=f"{municipality.name} Ward {int(ward[len(ward)-3:])}" #Assembling ward name to match format stored in db
                try:
                    ward_obj=Ward.objects.get(name=ward_name,municipality=municipality)
                except Ward.DoesNotExist:
                    print(f"Couldn't find: {ward_name}")
                    continue

                ward_data=municipality_data[ward]
                # Loading fields into db as ward details
                for version,_ in WardDetail.VERSION_CHOICES:
                    detail, _=WardDetail.objects.update_or_create(ward=ward_obj,field_name="councillor_name", stage=version,defaults={"field_value":ward_data["councillor"]["Name"],"field_type":"String"})
                    detail, _=WardDetail.objects.update_or_create(ward=ward_obj,field_name="councillor_political_party", stage=version,defaults={"field_value":ward_data["councillor"]["Affiliation"],"field_type":"String"})
                    detail, _=WardDetail.objects.update_or_create(ward=ward_obj,field_name="councillor_political_party_logo_url", stage=version,defaults={"field_value":ward_data["councillor"]["party"]["logo"],"field_type":"String"})
                    detail, _=WardDetail.objects.update_or_create(ward=ward_obj,field_name="councillor_contacts_phone", stage=version,defaults={"field_value":ward_data["councillor"]["party"]["telephone"],"field_type":"String"})
                    detail, _=WardDetail.objects.update_or_create(ward=ward_obj,field_name="councillor_party_representative", stage=version,defaults={"field_value":ward_data["councillor"]["party"]["representative"],"field_type":"String"})
                    detail, _=WardDetail.objects.update_or_create(ward=ward_obj,field_name="councillor_party_postal_address", stage=version,defaults={"field_value":ward_data["councillor"]["party"]["postal_address"],"field_type":"String"})
                    detail, _=WardDetail.objects.update_or_create(ward=ward_obj,field_name="councillor_website", stage=version,defaults={"field_value":ward_data["councillor"]["party"]["website"],"field_type":"String"})
                print(f"Saved: {ward_name}")





if __name__=="__main__":
    load_ward_details()     
