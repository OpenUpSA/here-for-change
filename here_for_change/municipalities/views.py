from django.views.generic import ListView, DetailView
from .models import Municipality, Ward, WardDetail as WardDetailModel
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

    def get_context_data(self, **kwargs):
        # get staging
        staging=self.request.GET.get("version","production")

        ctx= super().get_context_data(**kwargs)
        ward=self.get_object()
        ctx['ward_detail']={}

        ward_details=WardDetailModel.objects.filter(ward=ward,stage=staging)
        for detail in ward_details:
            ctx['ward_detail'][detail.field_name]={
                'value':detail.field_value
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
        
        ctx['neighbours']=[w.toDict() for w in  Ward.objects.filter(municipality=ward.municipality).exclude(pk=ward.pk)]
        return ctx


