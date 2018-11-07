from django.core.management.base import BaseCommand

try:
    # For Django running
    from vertex_app import models
except:
    # For PyCharm autocomplite only
    from django_project.vertex_app import models


class Command(BaseCommand):
    help = 'Init data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        sub_request_statuses = (
            ('created', 'создан'),
            ('error', 'ошибка исполнения'),
            ('processing', 'исполняется'),
            ('ready', 'готов')
        )
        sub_request_types = (
            ('ping', 'PING'),
            ('port', 'Открытый порт'),
            ('http', 'HTTP статус'),
        )
        try:
            for sub_request_status in sub_request_statuses:
                models.SubRequestStatus.objects.get_or_create(
                    code=sub_request_status[0],
                    name=sub_request_status[1]
                )
            for sub_request_type in sub_request_types:
                models.SubRequestType.objects.get_or_create(
                    code=sub_request_type[0],
                    name=sub_request_type[1]
                )
            self.stdout.write(self.style.SUCCESS('Successfully init'))
        except:
            raise
