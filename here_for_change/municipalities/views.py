from django.views.generic import ListView, DetailView
from .models import Municipality, Ward


class MunicipalityList(ListView):
    model = Municipality


class WardDetail(DetailView):
    model = Ward
    slug_field = 'slug__iexact'
    slug_url_kwarg = 'slug'
