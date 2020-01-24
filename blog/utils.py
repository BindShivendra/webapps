import random, logging, json
import string
from django.utils.text import slugify
from html.parser import HTMLParser


DONT_USE = ['new', 'myblogs ']

logger = logging.getLogger('app_api')

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
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return slug_generator(instance, new_slug=new_slug)
    return new_slug



class ImageHTMLParser(HTMLParser):

    def __init__(self, tag, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self._html = [] 
        self.remove_tag = tag.lower()

    def handle_starttag(self, tag, attrs):
        if tag.lower() != self.remove_tag:
            self._html.append(self.get_starttag_text())


    def handle_endtag(self, tag):
        if tag.lower() != self.remove_tag:
            self._html.append(f'</{tag}>')

    def handle_data(self, data):
        self._html.append(data)
    def get_data(self):
        ''' return html after removing tag '''
        return ''.join(self._html)


def remove_image(html):
    parser = ImageHTMLParser('img')
    parser.feed(html)
    logger.info('removing img tag')
    return parser.get_data()