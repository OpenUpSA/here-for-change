from functools import wraps
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geos import Point
from .models import Ward


def redirect_to_closest_ward(func):
    """
    Checks if a survey is available (published and not expired). Use this as a decorator for view functions.
    """

    @wraps(func)
    def to_closest_route(self, request, *args, **kwargs):
        ip=get_client_ip(request)
        gepIP=GeoIP2()
        if not request.COOKIES.get("closest_ward"):
            try:
                city=gepIP.city(ip)
                location=Point((city.get("latitude"),city.get("longitude")))
                closest_ward=Ward.objects.closest(location)
                res= redirect(closest_ward.get_absolute_url())
                res.set_cookie("closest_ward",f"{closest_ward.pk}")
                return res
            except:
                pass


        
        return func(self, request, *args, **kwargs)

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        elif request.META.get('HTTP_X_REAL_IP'):
            ip = request.META.get('HTTP_X_REAL_IP')
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    return to_closest_route


