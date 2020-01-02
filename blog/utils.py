import random
import string
from django.utils.text import slugify

DONT_USE = ['new', 'myblogs ']

def random_string_generator(size=10):
    chars=string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def slug_generator(instance, slug=None):

    if slug is not None:
        new_slug = slug
    else:
        new_slug = slugify(instance.title)
    
    if new_slug in DONT_USE:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
    
    class_name = instance.__class__
    qs_exists = class_name.objects.filter(slug=new_slug).exists()
    print(new_slug)
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return slug_generator(instance, new_slug=new_slug)
    return new_slug