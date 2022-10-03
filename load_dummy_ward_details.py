"""
This script loads dummy ward details for existing wards
"""

from django.contrib.gis.geos import MultiPolygon,Polygon
import os
import django
import random
from django.utils.timezone import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'here_for_change.settings')
django.setup()

from here_for_change.municipalities.models import (Ward,WardDetail)

DUMMY_DATA=[
    {
        'councillor': {
            'name': {
                'value': 'Danny Europa',
                'type': 'string',
                'updated': '2022/09/12 16:57'},
            'political_party': {
                'value': 'African National Congress (ANC)',
                'type': 'string',
                'updated': '2021/02/12 05:57'},
            'elected_date': {
                'value': datetime(2021, 1, 8),
                'type': 'date',
                'updated': '2022/09/12 16:57'},
            'contacts': {
                'email': {
                    'primary': {
                        'type': 'email',
                        'value': 'info@capeagulhas.co.za',
                        'updated': '2022/09/12 16:57',
                        'feedback': {'positive': 24, 'negative': 24}}
                },
                'phone': {
                    'value': '+27(0)284255500',
                    'type': 'phone',
                    'updated': '2022/09/12 16:57',
                    'feedback': {'positive': 5, 'negative': 0}
                },
            }
        }
    },
       
    {
        'councillor': {
            'name': {
                'value': 'Clever Harris',
                'type': 'string',
                'updated': '2022/09/12 16:57'},
            'political_party': {
                'value': 'Democratic Alliance Afrikaans (DA)',
                'type': 'string',
                'updated': '2021/02/12 05:57'},
            'elected_date': {
                'value': datetime(2022, 1, 8),
                'type': 'date',
                'updated': '2022/09/12 16:57'},
            'contacts': {
                'email': {
                    'primary': {
                        'type': 'email',
                        'value': 'info@capeagulhas.co.za',
                        'updated': '2022/09/12 16:57',
                        'feedback': {'positive': 14, 'negative': 24}}
                },
                'phone': {
                    'value': '+27(0)369255500',
                    'type': 'phone',
                    'updated': '2022/09/12 16:57',
                    'feedback': {'positive': 10, 'negative': 0}
                },
            }
        }
    },
    
    {
        'councillor': {
            'name': {
                'value': 'Jean Bulma',
                'type': 'string',
                'updated': '2022/09/12 16:57'},
            'political_party': {
                'value': 'Economic Freedom Fighters (EFF)',
                'type': 'string',
                'updated': '2021/02/12 05:57'},
            'elected_date': {
                'value': datetime(2019, 1, 8),
                'type': 'date',
                'updated': '2022/09/12 16:57'},
            'contacts': {
                'email': {
                    'primary': {
                        'type': 'email',
                        'value': 'info@capeagulhas.co.za',
                        'updated': '2022/09/12 16:57',
                        'feedback': {'positive': 20, 'negative': 4}}
                },
                'phone': {
                    'value': '+27(0)284255500',
                    'type': 'phone',
                    'updated': '2022/09/12 16:57',
                    'feedback': {'positive': 5, 'negative': 3}
                },
            }
        }
    },
    
    {
        'councillor': {
            'name': {
                'value': 'Clara Weatherman',
                'type': 'string',
                'updated': '2022/09/12 16:57'},
            'political_party': {
                'value': 'Economic Freedom Fighters (EFF)',
                'type': 'string',
                'updated': '2021/02/12 05:57'},
            'elected_date': {
                'value': datetime(2018, 1, 8),
                'type': 'date',
                'updated': '2022/09/12 16:57'},
            'contacts': {
                'email': {
                    'primary': {
                        'type': 'email',
                        'value': 'info@capeagulhas.co.za',
                        'updated': '2022/09/12 16:57',
                        'feedback': {'positive': 3, 'negative': 0}}
                },
                'phone': {
                    'value': '+27(0)284255500',
                    'type': 'phone',
                    'updated': '2022/09/12 16:57',
                    'feedback': {'positive': 1, 'negative': 4}
                },
            }
        }
    },
    
    {
        'councillor': {
            'name': {
                'value': 'Fitcher Jones',
                'type': 'string',
                'updated': '2022/09/12 16:57'},
            'political_party': {
                'value': 'Democratic Alliance Afrikaans (DA)',
                'type': 'string',
                'updated': '2021/02/12 05:57'},
            'elected_date': {
                'value': datetime(2017, 1, 8),
                'type': 'date',
                'updated': '2022/09/12 16:57'},
            'contacts': {
                'email': {
                    'primary': {
                        'type': 'email',
                        'value': 'info@capeagulhas.co.za',
                        'updated': '2022/09/12 16:57',
                        'feedback': {'positive': 30, 'negative': 12}}
                },
                'phone': {
                    'value': '+27(0)284255500',
                    'type': 'phone',
                    'updated': '2022/09/12 16:57',
                    'feedback': {'positive': 10, 'negative': 12}
                },
            }
        }
    },
    
    {
        'councillor': {
            'name': {
                'value': 'Emmanuel Malema',
                'type': 'string',
                'updated': '2022/09/12 16:57'},
            'political_party': {
                'value': 'African National Congress (ANC)',
                'type': 'string',
                'updated': '2021/02/12 05:57'},
            'elected_date': {
                'value': datetime(2018, 1, 8),
                'type': 'date',
                'updated': '2022/09/12 16:57'},
            'contacts': {
                'email': {
                    'primary': {
                        'type': 'email',
                        'value': 'info@capeagulhas.co.za',
                        'updated': '2022/09/12 16:57',
                        'feedback': {'positive': 19, 'negative': 10}}
                },
                'phone': {
                    'value': '+27(0)284255500',
                    'type': 'phone',
                    'updated': '2022/09/12 16:57',
                    'feedback': {'positive': 11, 'negative': 19}
                },
            }
        }
    },
]

def create_detail(ward:Ward,data:dict,stage:str="staging"):
    """
    Creates ward details for ward from data
    :param Ward ward: ward for which details should be created
    :param dict data: Dictionary containing fields to be added as ward detail
    :param dict stage: Version of details
    :rtype: None
    """
    for data_key in data.keys():
        for field_key in data[data_key].keys():
            field=data[data_key][field_key]
            print(field)
            if field_key=="elected_date":
                detail=WardDetail(ward=ward,field_name=f"{data_key}_{field_key}",field_type=field.get("type"),field_value=datetime.strftime(field.get("value"),r"%Y/%m/%d"),updated_at=datetime.strptime(field.get("updated"),r"%Y/%m/%d %H:%M"),stage=stage,feedback=field.get("feedback"))
                detail.save()
                
            elif field_key!="contacts":
                detail=WardDetail(ward=ward,field_name=f"{data_key}_{field_key}",field_type=field.get("type"),field_value=field.get("value"),updated_at=datetime.strptime(field.get("updated"),r"%Y/%m/%d %H:%M"),stage=stage,feedback=field.get("feedback"))
                detail.save()
            else:
                for contact_key in field.keys():

                    contact=field[contact_key]
                    if contact_key!="email":
                        detail=WardDetail(ward=ward,field_name=f"{data_key}_{field_key}_{contact_key}",field_type=contact.get("type"),field_value=contact.get("value"),updated_at=datetime.strptime(contact.get("updated"),r"%Y/%m/%d %H:%M"),stage=stage,feedback=contact.get("feedback"))
                        detail.save()
                    else:
                        for email_type in contact.keys():
                            email=contact[email_type]
                            detail=WardDetail(ward=ward,field_name=f"{data_key}_{field_key}_{contact_key}_{email_type}",field_type=email.get("type"),field_value=email.get("value"),updated_at=datetime.strptime(email.get("updated"),r"%Y/%m/%d %H:%M"),stage=stage,feedback=email.get("feedback"))
                            detail.save()





                        

if __name__=="__main__":
    WardDetail.objects.all().delete()
    versions=[WardDetail.STAGING,WardDetail.PRODUCTION]
    wards=Ward.objects.all()
    for ward in wards:
        for version in versions:
            create_detail(ward,DUMMY_DATA[random.randint(0,len(DUMMY_DATA))-1],version)



