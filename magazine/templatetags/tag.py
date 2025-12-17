import markdown
from django import template
from django.conf import settings
import re

register = template.Library()


@register.filter
def create_md(source):
    return markdown.Markdown(extensions=["fenced_code"]).convert(source)


# TODO: Figure out if we need to change this function - lerbsen
# It seems like the commented out part was the old one and the TODO was fixed???
def add_img_folder(folder):
    def add_img(filename):
        # return f"<img src=\"/static/{folder}/{filename}\" width=500>"
        # TODO EXPLICIT STATIC USED ie not static django tag
        return f'<img src="{settings.MEDIA_URL}{folder}{filename}"/>\n\n'

    return add_img


@register.filter(name="imgswitch")
def replace_double_braces(arg, folder):
    pattern = r"\{\{([^}]*)\}\}"
    replace = add_img_folder(folder)
    modified_text = re.sub(pattern, lambda x: replace(x.group(1)), arg)
    return modified_text


@register.filter
def imgremove(arg):
    return re.sub(r"\{\{.*?\}\}", "", arg)


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
