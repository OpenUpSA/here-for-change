from django.conf import settings

def ga4_tag(request):   
    return {"TAG_MANAGER_ENABLED":settings.TAG_MANAGER_ENABLED,"TAG_MANAGER_CONTAINER_ID":settings.TAG_MANAGER_CONTAINER_ID}
