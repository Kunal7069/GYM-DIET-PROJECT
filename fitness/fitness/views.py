from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.shortcuts import render
from model.models import *
import requests
from rest_framework.generics import ListAPIView

class NutritionEstimateView(ListAPIView):
    def get(self, request, *args, **kwargs):
        food_item = request.query_params.get("food")
        url = f'https://api.edamam.com/api/nutrition-data?app_id=21b4ee87&app_key=a0a287ed2537403d3c5b4a4d89e14091&nutrition-type=cooking&ingr={food_item}'
        response = requests.get(url).json()
        return HttpResponse(response)

class QuantityEstimateView(ListAPIView):
    def get(self, request, *args, **kwargs):
        food_item = "1 kg "+str(request.query_params.get("food"))
        nutrient = request.query_params.get("nutrient")
        required_nutrient_quantity = int(request.query_params.get("required_quantity"))
        url = f'https://api.edamam.com/api/nutrition-data?app_id=21b4ee87&app_key=a0a287ed2537403d3c5b4a4d89e14091&nutrition-type=cooking&ingr={food_item}'
        response = requests.get(url).json()
        return HttpResponse(str(required_nutrient_quantity/response['totalNutrients'][nutrient]['quantity']) +' kg')

class NutrientsWiseRecipeView(ListAPIView):
    def get(self, request, *args, **kwargs):
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByNutrients"
        querystring = {"limitLicense":"false","minProtein":"0","minVitaminC":"0","minSelenium":"0","maxFluoride":"50","maxVitaminB5":"50","maxVitaminB3":"50","maxIodine":"50","minCarbs":"0","maxCalories":"200","minAlcohol":"0","maxCopper":"50","maxCholine":"50","maxVitaminB6":"50","minIron":"0","maxManganese":"50","minSodium":"0","minSugar":"0","maxFat":"20","minCholine":"0","maxVitaminC":"400","maxVitaminB2":"50","minVitaminB12":"0","maxFolicAcid":"50","minZinc":"0","offset":"0","maxProtein":"100","minCalories":"0","minCaffeine":"0","minVitaminD":"0","maxVitaminE":"50","minVitaminB2":"0","minFiber":"0","minFolate":"0","minManganese":"0","maxPotassium":"50","maxSugar":"50","maxCaffeine":"50","maxCholesterol":"50","maxSaturatedFat":"50","minVitaminB3":"0","maxFiber":"50","maxPhosphorus":"50","minPotassium":"0","maxSelenium":"50","maxCarbs":"100","minCalcium":"0","minCholesterol":"0","minFluoride":"0","maxVitaminD":"50","maxVitaminB12":"50","minIodine":"0","maxZinc":"50","minSaturatedFat":"0","minVitaminB1":"0","maxFolate":"50","minFolicAcid":"0","maxMagnesium":"50","minVitaminK":"0","maxSodium":"50","maxAlcohol":"50","maxCalcium":"50","maxVitaminA":"50","maxVitaminK":"50","minVitaminB5":"0","maxIron":"50","minCopper":"0","maxVitaminB1":"50","number":"10","minVitaminA":"0","minPhosphorus":"0","minVitaminB6":"0","minFat":"5","minVitaminE":"0"}
        headers = {
            "X-RapidAPI-Key": "1af44b5713msh957ce7c530ad6aep123865jsn053a43fc74e8",
            "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring).json()
        print(len(response))
        ids=[]
        for i in response:
            ids.append(i['id'])
        print(ids)
        id=response[0]['id']
        result=[]
        for j in ids:
            url_2 = f'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{j}/information'
            headers = {
                "X-RapidAPI-Key": "1af44b5713msh957ce7c530ad6aep123865jsn053a43fc74e8",
                "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
            }
            response = requests.get(url_2, headers=headers).json()
            result.append({response['title'],response['instructions']})

        return Response(result)
    

class IndigreintsWiseRecipeView(ListAPIView):
    def get(self, request, *args, **kwargs):
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

        querystring = {"ingredients":"paneer,peas","number":"100","ignorePantry":"true","ranking":"1"}

        headers = {
            "X-RapidAPI-Key": "1af44b5713msh957ce7c530ad6aep123865jsn053a43fc74e8",
            "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        recipe_name=[]
        for i in response.json():
            recipe_name.append(i['title'])
        print(recipe_name)

        return Response(recipe_name)

def home(request):
    return render(request,"home.html")    

def submit(request):
    if request.method=='POST':
        name =request.POST.get('name')
        rollno =request.POST.get('rollno')
        en=Person(name=name,rollno=rollno)
        en.save()
        return render(request,"home.html")    
    