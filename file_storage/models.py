from django.db import models


# Create your models here.
class File(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    file_hash = models.CharField(max_length=64, unique=True, primary_key=True)
    file_path = models.FilePathField(null=True)
