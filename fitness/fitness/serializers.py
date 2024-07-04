from rest_framework import serializers
from model.models import *

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__' 

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__' 