from django.test import TestCase
from .models import Municipality


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
