import json
from django.test import Client, TestCase, TransactionTestCase
from django.http import JsonResponse
import html5lib
from .models import Municipality,Province,Ward

class IndexTestCase(TestCase):
    fixtures=["test-data.json"]
    def test_index(self):
        client = Client()
        response = client.get("/")
        self.assertContains(
            response, "Here For Change",
        )
        assertValidHTML(response.content.decode('utf-8'))

class JsonPagesTestCase(TransactionTestCase):
    fixtures=["test-data.json"]
    keys_in_response_ward=["ward_detail","neighbours","map_geoJson"]
    available_apps=["here_for_change.municipalities"]
    def test_ward_json_pages(self):   
        client=Client()
        wards=Ward.objects.all()
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

class ProvincetestCase(TestCase):
    available_apps=["here_for_change.municipalities"]
    fixtures=["test-data.json"]

    def setUp(self) -> None:
        self.test_province=Province.objects.create(name="Test Province 1",province_code="TP1",map_default_zoom=10)

    def test_province_create(self):
        p1 = Province.objects.get(name="Test Province 1")
        self.assertEqual(p1.province_code, 'TP1')

    def test_province_multiple_children(self):
        p1=Province.objects.get(name="Western Cape")
        p1_municipalities=Municipality.objects.filter(province=p1)
        self.assertEqual(len(p1.toDict(include_children=True)["children"]),p1_municipalities.count())

    def test_province_no_children(self):
        self.assertFalse(len(self.test_province.toDict(include_children=True)["children"])>0)

    def test_province_with_boundary(self):
        p1=Province.objects.get(name="Western Cape")
        self.assertIsNotNone(p1.toDict().get("map_geoJson"))



    
class MunicipalityTestCase(TestCase):
    available_apps=["here_for_change.municipalities"]
    fixtures=["test-data.json"]
    def setUp(self):
        p1=Province.objects.create(name="Test Province 2",province_code="TP2",map_default_zoom=10)
        self.test_municipality=Municipality.objects.create(name="Test Municipality",
                                    municipality_code="TM",
                                    municipality_type="Metropolitan",
                                    province=p1,
                                    map_default_zoom=10,)

    def test_municipality_create(self):
        m1 = Municipality.objects.get(name="Test Municipality")
        self.assertEqual(m1.municipality_code, 'TM')

    
    def test_municipality_multiple_children(self):
        m1=Municipality.objects.get(name="Bergrivier")
        m1_wards=Ward.objects.filter(municipality=m1)
        self.assertEqual(len(m1.toDict(include_children=True)["children"]),m1_wards.count())

    def test_municipality_no_children(self):
        self.assertFalse(len(self.test_municipality.toDict(include_children=True)["children"])>0)

    def test_municipality_with_boundary(self):
        m1=Municipality.objects.get(name="Bergrivier")
        self.assertIsNotNone(m1.toDict().get("map_geoJson"))
