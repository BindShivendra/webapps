from django.core.cache import cache
import logging, json

from blog.models import Post

logger = logging.getLogger('app_api')

class BlogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self,request, response):
        '''
            Add top five posts in response when user views "blog" 
        '''
        if 'blog' in request.path.split('/'):
            top_5 = cache.get('top_5', None)
            if top_5 is None:
                top_5 = Post.objects.published()[:5]
                cache.set('top_5',top_5)
                response.context_data['top_5'] = cache.get('top_5', None)
            else:
                response.context_data['top_5'] = cache.get('top_5', None)
            logger.info(response.context_data['top_5'])
        return response