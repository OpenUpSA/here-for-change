from django.views.generic import ListView, DetailView
from .models import Municipality, Ward
from datetime import datetime


class MunicipalityList(ListView):
    model = Municipality


class WardDetail(DetailView):
    model = Ward
    slug_field = 'slug__iexact'
    slug_url_kwarg = 'slug'
    page_content = {
        'ward': {
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
                        'feedback': {'positive': 5, 'negative': 0}},
                }
            }
        }
    }

    extra_context = {'content': page_content['ward']}
