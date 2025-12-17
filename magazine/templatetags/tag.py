from django import template

register = template.Library()


# Check if an article is really just an image article
# Image articles can have some caption, but for the article card we want to render them as just the image
@register.simple_tag
def is_image_article(arg: str):
    arg_striped = arg.strip()
    if arg_striped.startswith("{{"):
        if arg_striped.endswith("}}"):
            return True
        else:
            return len(arg.split()) <= 50
    return False


@register.filter
# usage: num|modulo:val
def modulo(num, val):
    return num % val


@register.filter
def trim_rh(arg: str):
    return arg.strip().removesuffix(".")
