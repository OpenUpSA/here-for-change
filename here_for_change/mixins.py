from django.conf import settings

class BaseViewContext():
    tags_object={"TAG_MANAGER_ENABLED":settings.TAG_MANAGER_ENABLED,"TAG_MANAGER_CONTAINER_ID":settings.TAG_MANAGER_CONTAINER_ID}

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context.update(self.tags_object)
        return context