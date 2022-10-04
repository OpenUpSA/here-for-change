from django.views.generic import ListView, DetailView, TemplateView
from .models import Municipality, Ward, WardDetail as WD
from datetime import datetime
from .decorators import redirect_to_closest_ward

class MunicipalityList(ListView):
    model = Municipality
    @redirect_to_closest_ward
    def get(self,request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


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
            },
        },
        'municipality': {
            'office_of_the_deputy_mayor': {
                'deputy_mayor': {
                    'name': {
                        'value': 'Ms Zukiswa Tonisi',
                        'type': 'string',
                        'updated': '2022/09/12 16:57',
                        'feedback': {'positive': 5, 'negative': 0}},
                    'contacts': {
                        'email': {
                            'primary': {
                                'type': 'email',
                                'value': 'pauls@capeagulhas.co.za',
                                'updated': '2022/09/12 16:57',
                                'feedback': {'positive': 5, 'negative': 0}}
                        },
                        'phone': {
                            'value': '+27(0)284255513',
                            'type': 'phone',
                            'updated': '2022/09/12 16:57',
                            'feedback': {'positive': 5, 'negative': 0}},
                    }
                },
                'secretary_deputy_mayor': {
                    'name': {
                        'value': 'Mr P Valentine',
                        'type': 'string',
                        'updated': '2022/09/12 16:57',
                        'feedback': {'positive': 5, 'negative': 0}},
                    'contacts': {
                        'email': {
                            'primary': {
                                'type': 'email',
                                'value': 'pauls@capeagulhas.co.za',
                                'updated': '2022/09/12 16:57',
                                'feedback': {'positive': 5, 'negative': 0}}
                        },
                        'phone': {
                            'value': '+27(0)284255513',
                            'type': 'phone',
                            'updated': '2022/09/12 16:57',
                            'feedback': {'positive': 5, 'negative': 0}},
                    }
                },
            }
        }
    }

    def get_context_data(self, **kwargs):
        # get staging
        staging=self.request.GET.get("version","production")

        ctx= super().get_context_data(**kwargs)
        #ctx['content']={}
        #ctx['content']['ward']=self.page_content['ward']
        
        object=self.get_object()
        ctx['versions']=[WD.STAGING,WD.PRODUCTION]
        ctx['selected_version']=staging
        ctx['ward_detail']={}
        ward_details=WD.objects.filter(ward=object,stage=staging)
        for detail in ward_details:
            print(detail.field_name)
            ctx['ward_detail'][detail.field_name]={
                'value':detail.field_value
            }
        
        ctx['neighbours']=Ward.objects.filter(municipality=object.municipality).exclude(pk=object.pk)
        return ctx

    extra_context = {'content': page_content}


class ArticleDetailView(TemplateView):
    template_name = "municipalities/map.html"
      
