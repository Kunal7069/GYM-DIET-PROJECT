from django.db import models
from django.utils import timezone
import uuid

    
class UserData(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password= models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob= models.DateField() 
    age=models.IntegerField()
    feet = models.FloatField(default=0)  
    inches = models.FloatField(default=0)  
    weight = models.FloatField()
    calorie = models.FloatField(default=0)
    carbs=models.FloatField(default=0) 
    proteins=models.FloatField(default=0) 
    fats=models.FloatField(default=0) 
    goal=models.CharField(max_length=100)
    desired_weight=models.IntegerField()
    activity_level=models.CharField(max_length=100,default='null')
    meals_per_day=models.IntegerField()

class Food(models.Model):
    food_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    recipe = models.CharField(max_length=10000)
    indigrients = models.EmailField(max_length=10000)
    food_calorie=models.FloatField(default=0) 
    food_carbs=models.FloatField(default=0) 
    food_proteins=models.FloatField(default=0) 
    food_fats=models.FloatField(default=0) 
    meal_type=models.CharField(max_length=100)
    
