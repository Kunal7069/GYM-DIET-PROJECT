import requests
from rest_framework.response import Response
string="6 Karela (Bitter Gourd/ Pavakkai) - deseeded,Salt - to taste,1 Onion - thinly sliced,3 tablespoon Gram flour (besan),2 teaspoons Turmeric powder (Haldi),1 tablespoon Red Chilli powder,2 teaspoons Cumin seeds (Jeera),1 tablespoon Coriander Powder (Dhania),1 tablespoon Amchur (Dry Mango Powder),Sunflower Oil - as required"
string_2=[]
str=''
for i in string:
    if i==',':
        string_2.append(str)
        str=''
    if i!=',':  
        str=str+i
print(string_2)
calorie=0
for i in string_2:
    food_item=i
    url = f'https://api.edamam.com/api/nutrition-data?app_id=21b4ee87&app_key=a0a287ed2537403d3c5b4a4d89e14091&nutrition-type=cooking&ingr={food_item}'
    response = requests.get(url).json()
    calorie=calorie+response['calories']
    # return Response(response['calories'])
print(calorie)
