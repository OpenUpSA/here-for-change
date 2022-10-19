from functools import wraps
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geos import Point
from .models import Ward


def redirect_to_closest_ward(func):
    """
    Gets the IP of the user from request and redirects to the closest ward.
    """

    @wraps(func)
    def to_closest_route(self, request, *args, **kwargs):
        user_ip=get_client_ip(request)
        geoIP=GeoIP2()
        if not request.COOKIES.get("closest_ward"):
            try:
                city=geoIP.city(user_ip)
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
            user_ip = x_forwarded_for.split(',')[-1].strip()
        elif request.META.get('HTTP_X_REAL_IP'):
            user_ip = request.META.get('HTTP_X_REAL_IP')
        else:
            user_ip = request.META.get('REMOTE_ADDR')
        return user_ip
    return to_closest_route


