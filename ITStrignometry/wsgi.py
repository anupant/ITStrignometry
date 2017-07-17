"""
WSGI config for ITStrignometry project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/



import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ITStrignometry.settings")

application = get_wsgi_application()
"""

import os
import sys


#path = '/home/pythonanywhereusername/projectname' #Use your own pythonanywhere username
path = '/home/curiouslearner/ITStrignometry'

if path not in sys.path:
    sys.path.append(path)

#os.environ['DJANGO_SETTINGS_MODULE'] = 'projectname.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = 'ITStrignometry.settings'

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(get_wsgi_application())