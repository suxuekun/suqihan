"""
WSGI config for suqihan project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

proj = os.path.dirname(__file__)
projs = os.path.dirname(proj)
if projs not in sys.path:
    sys.path.append(proj)
    sys.path.append(projs)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suqihan.settings")

application = get_wsgi_application()

print __name__,'start'
