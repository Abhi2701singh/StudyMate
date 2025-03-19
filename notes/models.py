from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()  # 1 for 1st year, 2 for 2nd year, etc.
    image = models.ImageField(upload_to='subject_images/', null=True, blank=True)
    is_quantum = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - Year {self.year}"

    class Meta:
        ordering = ['name']

class Chapter(models.Model):
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='chapter_images/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=200)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    file = models.FileField(upload_to='notes/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 