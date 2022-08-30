from django.views import generic
from django.views.generic import ListView, DetailView
from .models import Municipality, Ward


class MunicipalityList(ListView):
    model = Municipality


class MunicipalityDetail(DetailView):
    model = Municipality
    slug_field = 'municipality_code__iexact'
    slug_url_kwarg = 'municipality_code'


class WardDetail(DetailView):
    model = Ward
    slug_field = 'slug__iexact'
    slug_url_kwarg = 'slug'


class WardList(ListView):
    model = Ward
