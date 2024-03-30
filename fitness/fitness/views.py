from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.generics import ListAPIView

class ApiHitView(ListAPIView):
    def get(self, request, *args, **kwargs):
        url = 'https://api.edamam.com/api/nutrition-data?app_id=21b4ee87&app_key=a0a287ed2537403d3c5b4a4d89e14091&nutrition-type=cooking&ingr=1kg%20chicken'
        response = requests.get(url)
        return Response(response.json())
        