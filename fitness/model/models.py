from django.db import models
from django.utils import timezone
import uuid
class Person(models.Model):
    name = models.CharField(max_length=100)
    rollno = models.CharField(max_length=100)
    
class User(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

class water_consumtion(models.Model):
   user = models.ForeignKey(
        User, related_name="get_users", on_delete=models.CASCADE
    ) 
   water=models.IntegerField()
   date=models.DateField(null=True, default=timezone.now)