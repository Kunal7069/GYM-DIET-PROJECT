from django.contrib import admin
from .models import UserData,Food


class UserDataAdmin(admin.ModelAdmin):
    list_display=('id','first_name','last_name','email','password','gender','dob','age','feet','inches','weight','calorie','carbs','proteins','fats','goal','desired_weight','activity_level','meals_per_day')
admin.site.register(UserData,UserDataAdmin)

class FoodAdmin(admin.ModelAdmin):
    list_display=('food_id','name','recipe','indigrients','food_calorie','food_carbs','food_proteins','food_fats','meal_type')
admin.site.register(Food,FoodAdmin)
