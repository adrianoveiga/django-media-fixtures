from django.db import models

# Create your models here.
class FooModel(models.Model):
    description = models.CharField(max_length=200)
    image = models.FileField(upload_to='uploads/foomodel/img/', null=True, blank=True)