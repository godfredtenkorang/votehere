from django import template

register = template.Library()

@register.filter
def sum_attr(queryset, attr):
    return sum(getattr(item, attr) for item in queryset)

@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def multiply(value, arg):
    return float(value) * float(arg)