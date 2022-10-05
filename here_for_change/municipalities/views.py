from django.views.generic import ListView, DetailView
from .models import Municipality, Ward, WardDetail as WD
from datetime import datetime
from .decorators import redirect_to_closest_ward
from django.http import JsonResponse

class MunicipalityList(ListView):
    model = Municipality
    @redirect_to_closest_ward
    def get(self,request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class WardDetail(DetailView):
    model = Ward
    slug_field = 'slug__iexact'
    slug_url_kwarg = 'slug'
    # page_content = {
    #     'ward': {
    #         'councillor': {
    #             'name': {
    #                 'value': 'Danny Europa',
    #                 'type': 'string',
    #                 'updated': '2022/09/12 16:57'},
    #             'political_party': {
    #                 'value': 'African National Congress (ANC)',
    #                 'type': 'string',
    #                 'updated': '2021/02/12 05:57'},
    #             'elected_date': {
    #                 'value': datetime(2021, 1, 8),
    #                 'type': 'date',
    #                 'updated': '2022/09/12 16:57'},
    #             'contacts': {
    #                 'email': {
    #                     'primary': {
    #                         'type': 'email',
    #                         'value': 'info@capeagulhas.co.za',
    #                         'updated': '2022/09/12 16:57',
    #                         'feedback': {'positive': 24, 'negative': 24}}
    #                 },
    #                 'phone': {
    #                     'value': '+27(0)284255500',
    #                     'type': 'phone',
    #                     'updated': '2022/09/12 16:57',
    #                     'feedback': {'positive': 5, 'negative': 0}
    #                 },
    #             }
    #         }
    #     },
        

    # }

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
            ctx['ward_detail'][detail.field_name]={
                'value':detail.field_value
            }
        
        ctx['neighbours']=Ward.objects.filter(municipality=object.municipality).exclude(pk=object.pk)

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
        #{
        #    selected_version: staging or production,
        #    ward_detail:{},
        #    neighbours: List[ward.toJSON,*]
        # }

        ctx= {}
        object=self.get_object()
        ctx['selected_version']=staging
        ctx['ward_detail']={}
        ward_details=WD.objects.filter(ward=object,stage=staging)
        for detail in ward_details:
            ctx['ward_detail'][detail.field_name]={
                'value':detail.field_value
            }
        
        ctx['neighbours']=[w.toDict() for w in  Ward.objects.filter(municipality=object.municipality).exclude(pk=object.pk)]
        return ctx

