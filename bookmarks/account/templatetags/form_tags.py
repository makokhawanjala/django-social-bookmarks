from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter(name='add_placeholder')
def add_placeholder(field, placeholder):
    return field.as_widget(attrs={"placeholder": placeholder})

@register.filter(name='add_attrs')
def add_attrs(field, args):
    attrs = {}
    for arg in args.split(","):
        key, val = arg.split("=")
        attrs[key.strip()] = val.strip()
    return field.as_widget(attrs=attrs)