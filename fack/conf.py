from django.conf import settings


STORAGE = getattr(settings, 'FACK_STORAGE', None)
