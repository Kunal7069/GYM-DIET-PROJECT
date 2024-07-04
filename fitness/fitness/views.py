from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.shortcuts import render
from model.models import *
import requests
import json
from rest_framework.generics import ListAPIView
import pandas as pd
import http.client
from .serializers import *
import math

import re
from datetime import datetime
class NutritionEstimate1View(ListAPIView):
    def post(self, request, *args, **kwargs):
        data=request.data
        food_item=data['food']
        url = f'https://api.edamam.com/api/nutrition-data?app_id=21b4ee87&app_key=a0a287ed2537403d3c5b4a4d89e14091&nutrition-type=cooking&ingr={food_item}'
        response = requests.get(url).json()
        return Response(response['totalNutrients']['FAT']['quantity']+1)
class NutritionEstimateView(ListAPIView):
    def get(self, request, *args, **kwargs):
        file_path = 'C:/Users/jaink/Downloads/Book1.xlsx'
        df = pd.read_excel(file_path)
        recipes_list=df.iloc[:,0].tolist()
        nutrients=[]
        count=0
        for z in recipes_list:
            string_2=[]
            str=''
            for i in z:
                if i==',':
                    string_2.append(str)
                    str=''
                if i!=',':  
                    str=str+i
            calorie=0.00
            fats=0.00
            carbs=0.00
            proteins=0.00
            count=count+1
            print(count)
            nu=[]
            for i in string_2:
               
                url = f'https://api.edamam.com/api/nutrition-data?app_id=21b4ee87&app_key=a0a287ed2537403d3c5b4a4d89e14091&nutrition-type=cooking&ingr={i}'
                response = requests.get(url).json()
                try:
                    calorie=calorie+response['calories']
                except:
                    calorie=calorie
                try:
                    fats=fats+response['totalNutrients']['FAT']['quantity']
                except:
                    fats=fats
                try:    
                    carbs=carbs+response['totalNutrients']['CHOCDF']['quantity']
                except:
                    carbs=carbs
                try:
                    proteins=proteins+response['totalNutrients']['PROCNT']['quantity']
                except:
                    proteins=proteins
            nu.append(calorie)  
            nu.append(carbs)  
            nu.append(fats)  
            nu.append(proteins)    
            nutrients.append(nu)
        return Response(nutrients)
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

class SaveFood(ListAPIView):
    def get(self, request, *args, **kwargs):
        file_path = 'C:/Users/jaink/Desktop/GYM-DIET PROJECT/dinner.xlsx'
        df = pd.read_excel(file_path)
        food = df.iloc[:, 5:].values.tolist()
        print(food)
        for i in food:
            name = i[6]
            recipe = i[7]
            indigrients = i[5]
            food_calorie=round(i[0])
            food_carbs=round(i[1])
            food_proteins=round(i[3])
            food_fats=round(i[2])
            meal_type=i[4]
            en=Food(name=name,recipe=recipe,indigrients=indigrients,food_calorie=food_calorie,food_carbs=food_carbs,food_proteins=food_proteins,
                    food_fats=food_fats,meal_type=meal_type)
            en.save()
        return Response("LUNCH DISHES SAVED")
class SaveData(ListAPIView):
    def post(self, request, *args, **kwargs):
        data=request.data
        carbs=0
        proteins=0
        fats=0
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password= data['password']
        confirm_password=data['confirm_password']
        gender= data['gender']
        dob= data['dob']
        feet = data['feet'] 
        inches=data['inches']
        weight = data['weight']
        carbs=data['carbs']
        proteins=data['proteins']
        fats=data['fats']
        goal= data['goal']
        desired_weight= data['desired_weight']
        activity_level= data['activity_level']
        meals_per_day= data['meals_per_day']
        if password!=confirm_password:
           return Response("PASSWORD DO NOT MATCH") 
        if goal=='weight loss' and desired_weight>weight:
            return Response("IF YOU WANT TO LOSS WEGHT, DESIRED WEIGHT WILL BE LESS THAN THE ACTUAL WEIGHT")
        if goal=='weight gain' and desired_weight<weight:
            return Response("IF YOU WANT TO GAIN WEIGHT, DESIRED WEIGHT WILL BE MORE THAN THE ACTUAL WEIGHT")
        birthdate = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birthdate.year
        if (today.month, today.day) < (birthdate.month, birthdate.day):
            age -= 1
        url = "https://nutrition-calculator.p.rapidapi.com/api/nutrition-info"
        data={"measurement_units":"std","sex":gender,"age_value":age,"age_type":"yrs","feet":feet,"inches":inches,"lbs":weight,"activity_level":activity_level}
        headers = {
            "x-rapidapi-key": "1af44b5713msh957ce7c530ad6aep123865jsn053a43fc74e8",
            "x-rapidapi-host": "nutrition-calculator.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=data)
        result=response.json()
        calorie=result["BMI_EER"]["Estimated Daily Caloric Needs"]
        match = re.findall(r'\d+', calorie)
        calorie = int(''.join(match))
        if goal=='weight loss':
            calorie=calorie-400
        if goal=='weight gain':
            calorie=calorie+300
        if carbs==0:
            carbs=result["macronutrients_table"]["macronutrients-table"][1][1]
            matches = re.findall(r'\d+', carbs)
            numbers = [int(match) for match in matches]
            carbs = sum(numbers) / 2
        if proteins==0:    
            proteins=result["macronutrients_table"]["macronutrients-table"][3][1]
            match = re.findall(r'\d+', proteins)
            proteins = int(''.join(match))
        if fats==0:
            fats=result["macronutrients_table"]["macronutrients-table"][4][1]
            matches = re.findall(r'\d+', fats)
            numbers = [int(match) for match in matches]
            fats = sum(numbers) / 2
        
        en=UserData(first_name=first_name,last_name=last_name,email=email,password=password,gender=gender,dob=dob,
                    age=age,feet=feet,inches=inches,weight=weight,calorie=calorie,carbs=carbs,proteins=proteins,fats=fats,goal=goal,desired_weight=desired_weight,
                    activity_level=activity_level,meals_per_day=meals_per_day)
        
        en.save()
        return Response("DATA SAVED")

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
        result=response.json()
        
        calorie=result["BMI_EER"]["Estimated Daily Caloric Needs"]
        match = re.findall(r'\d+', calorie)
        calorie = int(''.join(match))

        carbs=result["macronutrients_table"]["macronutrients-table"][1][1]
        matches = re.findall(r'\d+', carbs)
        numbers = [int(match) for match in matches]
        carbs = sum(numbers) / 2
        
        
        proteins=result["macronutrients_table"]["macronutrients-table"][3][1]
        match = re.findall(r'\d+', proteins)
        proteins = int(''.join(match))
        
        fats=result["macronutrients_table"]["macronutrients-table"][4][1]
        matches = re.findall(r'\d+', fats)
        numbers = [int(match) for match in matches]
        fats = sum(numbers) / 2
        return Response(proteins)
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

class GetUser(ListAPIView):
    def get(self, request, *args, **kwargs):
        users=UserData.objects.all()
        serializer = UserDataSerializer(users, many=True)
        return Response(serializer.data)
    
class GetFood(ListAPIView):
    def post(self, request, *args, **kwargs):
        data=request.data
        meal_type=data['meal_type']
        food_calorie_min=data['food_calorie_min']
        food_calorie_max=data['food_calorie_max']
        foods=Food.objects.filter(food_calorie__lte=food_calorie_max,meal_type=meal_type,food_calorie__gt=food_calorie_min,food_carbs__gt=0,food_proteins__gt=0,food_fats__gt=0)
        serializer = FoodSerializer(foods, many=True)
        print(len(serializer.data))
        if len(serializer.data)==0:
            return Response("NO DISH AVAILABE")
        return Response(serializer.data)

