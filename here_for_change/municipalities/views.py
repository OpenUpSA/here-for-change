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
                'toc': {
                    'title': 'Ward Councillor',
                    'icon': 'fa-solid fa-person-half-dress',
                    'show': False
                },
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
            },
            'summary': {
                'toc': {
                    'title': 'Summary',
                    'icon': 'fa-solid fa-bolt-lightning',
                    'show': True
                },
            },
            'contacts': {
                'toc': {
                    'title': 'Contact',
                    'icon': 'fa-solid fa-phone-flip',
                    'show': True
                },
            },
            'spending': {
                'toc': {
                    'title': 'Spending',
                    'icon': 'fa-solid fa-coins',
                    'show': True
                },
            },
            'participation': {
                'toc': {
                    'title': 'Participation',
                    'icon': 'fa-solid fa-calendar-days',
                    'show': True
                },
                'items': [
                    {
                        'title': 'Find your ward councillor',
                        'url': 'https://www.elections.org.za/pw/Voter/Who-Is-My-Ward-Councillor',
                        'length': 20,
                        'likes': 142,
                        'replies': 184,
                        'popular': True,
                        'image': 'https://assets.website-files.com/61a46f92a4845f1ed45ec01d/61a714b84f3db51574f2f788_your-representative.jpg'
                    },
                    {
                        'title': 'Find your municipalities contact information',
                        'url': 'https://www.elections.org.za/pw/Voter/Who-Is-My-Ward-Councillor',
                        'length': 20,
                        'likes': 123,
                        'replies': 1083,
                        'popular': False,
                        'image': 'https://assets.website-files.com/61a46f92a4845f1ed45ec01d/61a719da17013bb1cdd7e7a9_image%2053.jpg'
                    },
                    {
                        'title': 'How does your municipality earn and spend its money',
                        'url': 'https://www.elections.org.za/pw/Voter/Who-Is-My-Ward-Councillor',
                        'length': 120,
                        'likes': 68,
                        'replies': 103,
                        'popular': True,
                        'image': 'https://assets.website-files.com/61a46f92a4845f1ed45ec01d/61a724522ad31c59960658bf_budget-spending.jpg'
                    },
                    {
                        'title': 'How your municipal and ward leadership was elected',
                        'url': 'https://www.elections.org.za/pw/Voter/Who-Is-My-Ward-Councillor',
                        'length': 120,
                        'likes': 241,
                        'replies': 205,
                        'popular': False,
                        'image': 'https://assets.website-files.com/61a46f92a4845f1ed45ec01d/61a722fba44a202e751b93b3_elections.jpg'
                    }
                ]
            },
            'surveys': {
                'toc': {
                    'title': 'Surveys',
                    'icon': 'fa-solid fa-file-signature',
                    'show': True
                },
            },
            'elections': {
                'toc': {
                    'title': 'Elections',
                    'icon': 'fa-solid fa-check-to-slot',
                    'show': True
                },
            },
            'messages': {
                'toc': {
                    'title': 'Messages',
                    'icon': 'fa-solid fa-comment-dots',
                    'show': True
                },
            }
        }
    }

    extra_context = {'content': page_content['ward']}
