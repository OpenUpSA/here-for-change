from django import template

register = template.Library()

@register.filter(name='order_by')
def order_by(queryset,field):
    return queryset.order_by(field)

@register.filter(name='order_wards')
def order_wards(queryset):
    sorted_wards=sorted(queryset,key=lambda x: int(x.formatted_name.split(" ")[1]))
    return sorted_wards