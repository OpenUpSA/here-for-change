from datetime import datetime
import json

from django.contrib.gis.geos import Point
from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, View
from .models import Municipality, Ward
from .models import WardDetail as WardDetailModel

from .forms import FindMyWardCouncillorFeedbackForm
from ..mixins import BaseViewContext


class Home(BaseViewContext,ListView):
    model = Municipality
    template_name = "municipalities/home.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["object_list"]=[municipality.toDict(include_children=True) for municipality in  Municipality.objects.filter(name__in=['City of Cape Town','Bergrivier'])]
        return ctx



class WardDetail(BaseViewContext,DetailView):
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
        staging = self.request.GET.get("version", "production")

        ctx = super().get_context_data(**kwargs)
        ctx.update(self.tags_object)
        ward = self.get_object()
        ctx['ward_detail'] = {}

        ward_details = WardDetailModel.objects.filter(ward=ward, stage=staging)
        for detail in ward_details:
            ctx['ward_detail'][detail.field_name] = {
                'value': detail.field_value,
                'feedback': detail.feedback
            }
        ctx['neighbours'] = []
        for neighbour_ward in Ward.objects.filter(municipality=ward.municipality).exclude(pk=ward.pk):
            ward_details = WardDetailModel.objects.filter(
                ward=neighbour_ward, stage=staging)
            data = neighbour_ward.toDict()
            data['ward_detail'] = {}
            for detail in ward_details:
                data['ward_detail'][detail.field_name] = {
                    'value': detail.field_value,
                    'updated_at': detail.updated_at.isoformat(),
                    'feedback': detail.feedback
                }
            ctx['neighbours'].append(data)
        return ctx


class WardDetailJson(DetailView):
    model = Ward
    slug_field = 'slug__iexact'
    slug_url_kwarg = 'slug'

    def get(self, request, municipality_code, slug):
        super().get(request, municipality_code, slug)
        ctx = self.get_context_data()
        return JsonResponse(ctx, safe=False)

    def get_context_data(self, **kwargs):
        # get staging
        staging = self.request.GET.get("version", "production")
        ctx = {}
        ward = self.get_object()
        ctx.update(ward.toDict())
        ctx['ward_detail'] = {}
        ward_details = WardDetailModel.objects.filter(ward=ward, stage=staging)
        for detail in ward_details:
            ctx['ward_detail'][detail.field_name] = {
                'value': detail.field_value,
                'updated_at': detail.updated_at.isoformat(),
                'feedback': detail.feedback
            }
        ctx['neighbours'] = []
        for neighbour_ward in Ward.objects.filter(municipality=ward.municipality).exclude(pk=ward.pk):
            ward_details = WardDetailModel.objects.filter(
                ward=neighbour_ward, stage=staging)
            data = neighbour_ward.toDict()
            data['ward_detail'] = {}
            for detail in ward_details:
                data['ward_detail'][detail.field_name] = {
                    'value': detail.field_value,
                    'updated_at': detail.updated_at.isoformat(),
                    'feedback': detail.feedback
                }
            ctx['neighbours'].append(data)
        return ctx


class MunicipalityDetailJson(BaseViewContext,DetailView):
    model = Municipality
    slug_field = 'municipality_code'
    slug_url_kwarg = 'municipality_code'

    def get(self, request, municipality_code):
        super().get(request, municipality_code)
        ctx = self.get_context_data()
        return JsonResponse(ctx, safe=False)

    def get_context_data(self, **kwargs):
        municipality = self.get_object()
        ctx = municipality.toDict()
        ctx.update(self.tags_object)
        municipality_location = Point(
            (municipality.map_latitude, municipality.map_longitude))
        ctx['neighbours'] = [municipality_neighbor.toDict(
        ) for municipality_neighbor in Municipality.objects.closest_n(municipality_location, municipality, 5)]
        return ctx


class FindMyWardCouncillor(BaseViewContext,ListView):
    template_name = "municipalities/find_my_ward_councillor.html"
    model = Municipality

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["object_list"]=[municipality.toDict(include_children=True) for municipality in  Municipality.objects.filter(name__in=['City of Cape Town','Bergrivier'])]
        return ctx

class WhoIsMyWardCouncillor(BaseViewContext,DetailView):
    model = Ward
    template_name = "municipalities/who_is_my_ward_councillor.html"
    slug_field = 'slug__iexact'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        # get staging
        staging = self.request.GET.get("version", "production")

        ctx = super().get_context_data(**kwargs)
        ctx.update(self.tags_object)
        ward = self.get_object()
        ctx['ward_detail'] = {}

        ward_details = WardDetailModel.objects.filter(ward=ward, stage=staging)
        for detail in ward_details:
            ctx['ward_detail'][detail.field_name] = {
                'value': detail.field_value,
                'feedback': detail.feedback
            }

        ctx['neighbours'] = []
        for neighbour_ward in Ward.objects.filter(municipality=ward.municipality).exclude(pk=ward.pk):
            ward_details = WardDetailModel.objects.filter(
                ward=neighbour_ward, stage=staging)
            data = neighbour_ward.toDict()
            data['ward_detail'] = {}
            for detail in ward_details:
                data['ward_detail'][detail.field_name] = {
                    'value': detail.field_value,
                    'updated_at': detail.updated_at.isoformat(),
                    'feedback': detail.feedback
                }
            ctx['neighbours'].append(data)
        return ctx


class RedirectClosestWard(View):
    def get(self, request):
        longitude, latitude = (request.GET.get(
            "longitude"), request.GET.get("latitude"))
        input_url = request.GET.get("url")
        if longitude and latitude:
            location = Point((float(latitude), float(longitude)))
            closest_ward = Ward.objects.closest(location)
            if input_url.endswith("find-my-ward-councillor"):
                return redirect(closest_ward.get_absolute_url() + "ward-councillor")
            else:
                return redirect(closest_ward.get_absolute_url())
        else:
            return redirect("home")


class Feedback(View):
    def post(self, request):
        form_data = json.loads(request.body)
        form = FindMyWardCouncillorFeedbackForm(form_data)
        if form.is_valid():
            form.save()
            res = {
                "status": "success",
                "email": form_data.get('email'),
                "feedback": form_data.get('feedback')
            }
        else:
            res = {
                "status": "failed",
                "error": form.errors
            }

        return JsonResponse(res, safe=False)


class UpdateWardDetailFeedback(View):
    def post(self, request, ward_slug, field):
        updated = False
        data = dict(json.loads(request.body))
        action = data.get("action")
        if not action:
            return HttpResponseBadRequest()
        # Get info on last action performed by user
        last_feedback = request.COOKIES.get(f"{ward_slug}-{field}")
        try:
            ward_detail = WardDetailModel.objects.get(
                ward__slug=ward_slug, field_name=field, stage="production")  # get Ward detail
        except WardDetailModel.DoesNotExist:
            return Http404()
        if last_feedback:
            last_feedback = json.loads(last_feedback)
            last_action = last_feedback.get("action")
            if action != last_action:  # If current and last action are different, reduce last action number and increase current action number
                ward_detail.feedback[last_action] -= 1
                ward_detail.feedback[action] += 1
                updated = True
        else:
            # increase current action
            ward_detail.feedback[action] += 1
            updated = True

        if updated:
            ward_detail.save()
            response = JsonResponse(
                {"updated": updated, "feedback": ward_detail.feedback})
            # Save performed action as last action in cookie
            response.set_cookie(f"{ward_slug}-{field}", json.dumps(
                {"action": action, "updated": datetime.now().timestamp()}))
            return response
        return JsonResponse({"updated": updated})
