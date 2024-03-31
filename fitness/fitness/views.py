from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
import requests
from rest_framework.generics import ListAPIView

class NutritionEstimateView(ListAPIView):
    def get(self, request, *args, **kwargs):
        food_item = request.query_params.get("food")
        url = f'https://api.edamam.com/api/nutrition-data?app_id=21b4ee87&app_key=a0a287ed2537403d3c5b4a4d89e14091&nutrition-type=cooking&ingr={food_item}'
        response = requests.get(url).json()
        return Response(response)

class QuantityEstimateView(ListAPIView):
    def get(self, request, *args, **kwargs):
        food_item = "1 kg "+str(request.query_params.get("food"))
        nutrient = request.query_params.get("nutrient")
        required_nutrient_quantity = int(request.query_params.get("required_quantity"))
        url = f'https://api.edamam.com/api/nutrition-data?app_id=21b4ee87&app_key=a0a287ed2537403d3c5b4a4d89e14091&nutrition-type=cooking&ingr={food_item}'
        response = requests.get(url).json()
        
        return Response(str(required_nutrient_quantity/response['totalNutrients'][nutrient]['quantity']) +' kg')
 
       