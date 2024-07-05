"""
URL configuration for fitness project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import path
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('nutrition_api/',NutritionEstimateView.as_view(),name="nutrition_estimate"),
    path('calorie_intake/',CalorieIntake.as_view(),name="calorie_intake"),
    path('calorie_distribution/',CalorieDistribution.as_view(),name="calorie_distribution"),
    path('similar_food/',SimilarFood.as_view(),name="similar_food"),
    path('quantity_api/',QuantityEstimateView.as_view(),name="quantity_estimate"),
    path('recipe_api/',NutrientsWiseRecipeView.as_view(),name="recipe_estimate"),
    path('integrients_recipe_api/',IndigreintsWiseRecipeView.as_view(),name="integrients_recipe_api"),
    path('save_data/',SaveData.as_view(),name="save_data"),
    path('save_food/',SaveFood.as_view(),name="save_food"),
    path('get_user/',GetUser.as_view(),name="get_user"),
    path('get_food/',GetFood.as_view(),name="get_food"),
    path('image_food/',ImageFood.as_view(),name="image_food"),
    path('bmi_estimate_api/',BMIEstimateView.as_view(),name="bmi_estimate"),
    
]
