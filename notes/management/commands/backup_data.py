from django.core.management.base import BaseCommand
from django.core import serializers
from notes.models import Subject, Chapter, Note

class Command(BaseCommand):
    help = 'Backup all data'

    def handle(self, *args, **kwargs):
        with open('data_backup.json', 'w') as f:
            serializers.serialize('json', Subject.objects.all(), stream=f)
            serializers.serialize('json', Chapter.objects.all(), stream=f)
            serializers.serialize('json', Note.objects.all(), stream=f) 