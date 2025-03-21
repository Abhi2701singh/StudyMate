from django.core import serializers
from notes.models import Subject, Chapter, Note

# Export data
with open('data_backup.json', 'w') as f:
    serializers.serialize('json', Subject.objects.all(), stream=f)
    serializers.serialize('json', Chapter.objects.all(), stream=f)
    serializers.serialize('json', Note.objects.all(), stream=f)

# After migrations, import data
with open('data_backup.json', 'r') as f:
    for obj in serializers.deserialize('json', f):
        obj.save() 