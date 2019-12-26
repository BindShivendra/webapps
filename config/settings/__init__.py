from .base import *

try:
    from .blog_settings import *
except:
    pass

try:
    from .local_settings import *
except:
    pass

try:
    from .prod_settings import *
except:
    pass


