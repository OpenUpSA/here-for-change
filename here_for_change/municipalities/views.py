from datetime import datetime

from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, View

from .decorators import redirect_to_closest_ward
from .models import Municipality, Ward
from .models import WardDetail as WardDetailModel


class Home(ListView):
    model = Municipality
    template_name = "municipalities/home.html"
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

    extra_context = {'content': page_content}

    def get_context_data(self, **kwargs):
        # get staging
        staging=self.request.GET.get("version","production")

        ctx= super().get_context_data(**kwargs)
        ward=self.get_object()
        ctx['ward_detail']={}

        ward_details=WardDetailModel.objects.filter(ward=ward,stage=staging)
        for detail in ward_details:
            ctx['ward_detail'][detail.field_name]={
                'value':detail.field_value,
                'feedback':detail.feedback
            }
        
        ctx['neighbours']=Ward.objects.filter(municipality=ward.municipality).exclude(pk=ward.pk)
        return ctx


class WardDetailJson(DetailView):
    model = Ward
    slug_field = 'slug__iexact'
    slug_url_kwarg = 'slug'

    def get(self,request,municipality_code,slug):
        super().get(request,municipality_code,slug)
        ctx=self.get_context_data()
        return JsonResponse(ctx,safe=False)


    def get_context_data(self, **kwargs):
        # get staging
        staging=self.request.GET.get("version","production")
        ctx= {}
        ward=self.get_object()
        ctx.update(ward.toDict())
        ctx['ward_detail']={}
        ward_details=WardDetailModel.objects.filter(ward=ward,stage=staging)
        for detail in ward_details:
            ctx['ward_detail'][detail.field_name]={
                'value':detail.field_value,
                'updated_at':detail.updated_at
            }
        
        ctx['neighbours']=[wrd.toDict() for wrd in  Ward.objects.filter(municipality=ward.municipality).exclude(pk=ward.pk)]
        return ctx


      
class FindMyWardCouncillor(ListView):
    template_name = "municipalities/find_my_ward_councillor.html"
    model = Municipality


class RedirectClosestWard(View):
    def get(self,request):
        longitude,latitude=(request.GET.get("longitude"),request.GET.get("latitude"))
        if longitude and latitude:
            print(float(latitude),float(longitude))
            location=Point((float(latitude),float(longitude)))
            closest_ward=Ward.objects.closest(location)
            return redirect(closest_ward.get_absolute_url())
        else:
            return redirect("home")

