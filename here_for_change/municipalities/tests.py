import json
from django.test import Client, TestCase
from django.http import JsonResponse
import html5lib
from .models import Municipality

from .models import Ward
import load_dummy_ward_details,load_wards
from django.core.management import call_command


class IndexTestCase(TestCase):
    def test_index(self):
        client = Client()
        response = client.get("/")
        self.assertContains(
            response, "Here For Change",
        )
        assertValidHTML(response.content)

class JsonPagesTestCase(TestCase):
    keys_in_response_ward=["ward_detail","neighbours"]
    def test_ward_json_pages(self):   
        client=Client()
        loadDbData()
        wards=Ward.objects.using("default").all()
        for ward in wards:
            response=client.get(ward.toJsonUrl())
            self.assertEqual(response.__class__,JsonResponse,msg="Response object is not JsonResponse")
            data=json.loads(response.content)
            for key in self.keys_in_response_ward:
                self.assertIn(key,data.keys(),msg=f"Necessary key {key} missen in response content")


def assertValidHTML(string):
    """
    Raises exception if the string is not valid HTML, e.g. has unmatched tags
    that need to be matched.
    """
    parser = html5lib.HTMLParser(strict=True)
    parser.parse(string)

def loadDbData():
    """
    Loads db with data needed for tests
    """
    #Load fixtures
    call_command('loaddata', 'demo-data.json')

    #Load Wards
    load_wards.load_wards()

    #load Ward details
    load_dummy_ward_details.load_dummy_ward_details()
    
class MunicipalityTestCase(TestCase):
    def setUp(self):
        Municipality.objects.create(name="City of Cape Town",
                                    municipality_code="CPT",
                                    municipality_type="Metropolitan",
                                    province="WesternCape",
                                    map_default_zoom=10,
                                    map_latitude="-33.9249000",
                                    map_longitude="18.4241000")

    def test_municipality(self):
        m1 = Municipality.objects.get(name="City of Cape Town")
        self.assertEqual(m1.municipality_code, 'CPT')
