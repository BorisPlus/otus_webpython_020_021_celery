# Celery configuration file
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
#
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

CELERY_IMPORTS = ("jobs", )
CELERY_REDIRECT_STDOUTS_LEVEL = 'INFO'
