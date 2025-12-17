from django import template

register = template.Library()


@register.filter
# usage: num|modulo:val
def modulo(num, val):
    return num % val


@register.filter
def trim_rh(arg: str):
    return arg.strip().removesuffix(".")
