from django.core.management.base import BaseCommand
from django.core import serializers

class Command(BaseCommand):
    help = 'Restore data from backup'

    def handle(self, *args, **kwargs):
        with open('data_backup.json', 'r') as f:
            for obj in serializers.deserialize('json', f):
                obj.save() 