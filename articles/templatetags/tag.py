import markdown
from django import template
from django.conf import settings
import re
register = template.Library()

def create_md(source):
    #return source
    return markdown.Markdown(extensions=["fenced_code"]).convert(source)


def add_img_folder(folder):
    def add_img(filename):
        #return f"<img src=\"/static/{folder}/{filename}\" width=500>"
        # TODO EXPLICIT STATIC USED ie not static django tag
        return f"<img src=\"{settings.MEDIA_URL}{folder}{filename}\" style=\"width: 50%; margin-left: 25%; height: auto;\"><br>\n\n"
    return add_img

def replace_double_braces(arg, folder):
    # print(f"got folder: {folder}") # "first" arg
    # print(f"got arg: {arg}") # the content that was piped in
    pattern = r'\{\{([^}]*)\}\}'
    replace = add_img_folder(folder)
    modified_text = re.sub(pattern, lambda x: replace(x.group(1)), arg)
    return modified_text

def imgremove(arg):
    return re.sub(r'\{\{.*?\}\}', "", arg)


def is_image_article(arg: str):
    arg = arg.strip()
    return arg.startswith("{{") and arg.endswith("}}")

@register.filter
def modulo(num, val):
    return num % val

register.filter("create_md", create_md)
register.filter("imgswitch", replace_double_braces)
register.filter("imgremove", imgremove)
register.simple_tag(is_image_article)