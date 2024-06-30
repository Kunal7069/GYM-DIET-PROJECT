from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.shortcuts import render
from model.models import *
import requests
from rest_framework.generics import ListAPIView
import pandas as pd
import http.client

# class NutritionEstimateView(ListAPIView):
#     def post(self, request, *args, **kwargs):
#         data=request.data
#         food_item=data['food']
#         url = f'https://api.edamam.com/api/nutrition-data?app_id=21b4ee87&app_key=a0a287ed2537403d3c5b4a4d89e14091&nutrition-type=cooking&ingr={food_item}'
#         response = requests.get(url).json()
#         return Response(response['calories'])
class NutritionEstimateView(ListAPIView):
    def get(self, request, *args, **kwargs):
        file_path = 'C:/Users/jaink/Downloads/Book1.xlsx'
        df = pd.read_excel(file_path)
        recipes_list=df.iloc[:,0].tolist()
        calories=[]
        for z in recipes_list:
            string_2=[]
            str=''
            for i in z:
                if i==',':
                    string_2.append(str)
                    str=''
                if i!=',':  
                    str=str+i
            print(string_2)
            calorie=0
            for i in string_2:
                url = f'https://api.edamam.com/api/nutrition-data?app_id=21b4ee87&app_key=a0a287ed2537403d3c5b4a4d89e14091&nutrition-type=cooking&ingr={i}'
                response = requests.get(url).json()
                calorie=calorie+response['calories']
            calories.append(calorie)
            # return Response(response['calories'])
        return Response(calories)
class SimilarFood(ListAPIView):
    def post(self, request, *args, **kwargs):
        data=request.data
        food_item=data['food']
        url = f'https://api.edamam.com/api/nutrition-data?app_id=21b4ee87&app_key=a0a287ed2537403d3c5b4a4d89e14091&nutrition-type=cooking&ingr={food_item}'
        response = requests.get(url).json()
        calories=response['calories']
        
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByNutrients"

        querystring = {"limitLicense":"false","maxCalories":calories+10,"minCalories":calories-10}

        headers = {
            "x-rapidapi-key": "1af44b5713msh957ce7c530ad6aep123865jsn053a43fc74e8",
            "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

        response_2 = requests.get(url, headers=headers, params=querystring)
        return Response(response_2.json())
class QuantityEstimateView(ListAPIView):
    def post(self, request, *args, **kwargs):
        data=request.data
        food=data['food']
        nutrient = data['nutrient']
        required_nutrient_quantity = data['required_nutrient_quantity']
        food_item = "1 kg "+str(food)
        url = f'https://api.edamam.com/api/nutrition-data?app_id=21b4ee87&app_key=a0a287ed2537403d3c5b4a4d89e14091&nutrition-type=cooking&ingr={food_item}'
        response = requests.get(url).json()
        return HttpResponse(str(required_nutrient_quantity/response['totalNutrients'][nutrient]['quantity']) +' kg')

class CalorieDistribution(ListAPIView):
    def post(self, request, *args, **kwargs):
        data=request.data
        calorie=data['calorie']
        meals=data['meals']
        if meals==3:
            breakfast_lower=0.3*calorie
            breakfast_upper=0.35*calorie
            lunch_lower=0.35*calorie
            lunch_upper=0.40*calorie
            dinner_lower=0.25*calorie
            dinner_upper=0.35*calorie
            response={'breakfast_lower':breakfast_lower,'breakfast_upper':breakfast_upper,'lunch_lower':lunch_lower,'lunch_upper':lunch_upper,'dinner_lower':dinner_lower,'dinner_upper':dinner_upper}
        elif meals==4:
            breakfast_lower=0.25*calorie
            breakfast_upper=0.3*calorie
            morning_snack_lower=0.05*calorie
            morning_snack_upper=0.1*calorie
            lunch_lower=0.35*calorie
            lunch_upper=0.40*calorie
            dinner_lower=0.25*calorie
            dinner_upper=0.3*calorie
            response={'breakfast_lower':breakfast_lower,'breakfast_upper':breakfast_upper,'morning_snack_lower':morning_snack_lower,'morning_snack_upper':morning_snack_upper,'lunch_lower':lunch_lower,'lunch_upper':lunch_upper,'dinner_lower':dinner_lower,'dinner_upper':dinner_upper}
        elif meals==5:
            breakfast_lower=0.25*calorie
            breakfast_upper=0.3*calorie
            morning_snack_lower=0.05*calorie
            morning_snack_upper=0.1*calorie
            lunch_lower=0.35*calorie
            lunch_upper=0.40*calorie
            afternoon_snack_lower=0.05*calorie
            afternoon_snack_upper=0.1*calorie
            dinner_lower=0.15*calorie
            dinner_upper=0.2*calorie
            response={'breakfast_lower':breakfast_lower,'breakfast_upper':breakfast_upper,'morning_snack_lower':morning_snack_lower,'morning_snack_upper':morning_snack_upper,'lunch_lower':lunch_lower,'lunch_upper':lunch_upper,'afternoon_snack_lower':afternoon_snack_lower,'afternoon_snack_upper':afternoon_snack_upper,'dinner_lower':dinner_lower,'dinner_upper':dinner_upper}
        return Response(response)
class CalorieIntake(ListAPIView):
    def post(self, request, *args, **kwargs):
        url = "https://nutrition-calculator.p.rapidapi.com/api/nutrition-info"
        data=request.data
        headers = {
            "x-rapidapi-key": "1af44b5713msh957ce7c530ad6aep123865jsn053a43fc74e8",
            "x-rapidapi-host": "nutrition-calculator.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=data)
        return Response(response.json())
class BMIEstimateView(ListAPIView):
    def post(self, request, *args, **kwargs):
        data=request.data
        url = "https://fitness-calculator.p.rapidapi.com/dailycalorie"
        headers = {
            "X-RapidAPI-Key": "1af44b5713msh957ce7c530ad6aep123865jsn053a43fc74e8",
            "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=data).json()
        print(response.json())
        return Response(response)

class NutrientsWiseRecipeView(ListAPIView):
    def post(self, request, *args, **kwargs):
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByNutrients"
        querystring = request.data 
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
    def post(self, request, *args, **kwargs):
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"
        data=request.data
        querystring = data

        headers = {
            "X-RapidAPI-Key": "1af44b5713msh957ce7c530ad6aep123865jsn053a43fc74e8",
            "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        print(response)
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
    