import base64
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from .models import DiseaseSuggestion
from django.db import transaction
import requests
import json
import logging
from planta.models import Ingredient, Recepy, IngredientRecepy, DiseaseSuggestion
from decouple import config

headers_plant = {
'Api-Key': config('Head_Plant'),
'Content-Type': 'application/json'
}

headers_spoon = {
  'x-api-key': config('Head_Spoon'),
  'Content-Type': 'application/json'
}


def imagefield_to_base64(image_field):
    with image_field.open('rb') as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data)
        base64_string = base64_data.decode('utf-8')
        return base64_string

def save_plant_desease(health_instance,data_health):
    with transaction.atomic():
        print('Desease list_____')
        for hd in data_health['result']['disease']['suggestions']:  
            print(f" instnace: {health_instance}")
            print(f" id: {hd['id']}")
            print(f" name: {hd['name']}")
            print(f" probability: {hd['probability']}")
            print(f" description: {hd['details']['description']}")
            print(f" url: {hd['details']['url']}")
            print(f" treatment_chemical: {hd.get('details', {}).get('treatment',{}).get('chemical','')}")
            print(f" treatment_biological: {hd.get('details', {}).get('treatment',{}).get('biological','')}")
            print(f" prevention: {hd.get('details', {}).get('treatment',{}).get('prevention','')}")
            print(f" common_names_disease: {hd.get('details', {}).get('common_names','')}")
            print(f" cause: {hd.get('details', {}).get('cause','')}")
            try:     
                DiseaseSuggestion.objects.create(
                    disease_health_assessment = health_instance,
                    disease_id_DiseaseSuggestion = hd['id'],
                    disease_name = hd['name'],
                    disease_probability = hd['probability'],
                    disease_description = hd['details']['description'],
                    disease_url = hd['details']['url'],
                    disease_treatment_chemical = hd.get('details', {}).get('treatment',{}).get('chemical',''),
                    disease_treatment_biological = hd.get('details', {}).get('treatment',{}).get('biological',''),
                    disease_prevention = hd.get('details', {}).get('treatment',{}).get('prevention',''),
                    disease_common_names_disease = hd.get('details', {}).get('common_names',''),
                    disease_cause = hd.get('details', {}).get('cause',''),  
                )
                print(f"Disease saved :  {hd['name']}") 
            except ValidationError as e:
                print(f"Validation Error: {e.message_dict}")
            except IntegrityError as e:
                print(f"Integrity Error: {e}")
            except DatabaseError as e:
                print(f"Database Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")  
        print('_____')


def save_recepy(ing_n):
    print('_____')
    ingr = Ingredient.objects.filter(ingredient_original_name=ing_n).first()
    print(f"running api for ingredient with name {ing_n}")
    
    # with transaction.atomic():
    number = 3
    ranking = 1
    url_recepy = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingr}&number={number}&ranking={ranking}"
    response_recepy = requests.get(url_recepy, headers=headers_spoon)
    data_recepy = response_recepy.json()        

    for recipe in data_recepy:
        try:
            print(f" id_recepy : {recipe['id']}")
            print(f" title: {recipe['title']}")
            print(f" image : {recipe['image']}")
            print(f" used_ingredient_count : {recipe['usedIngredientCount']}")
            print(f" missed_ingredient_count : {recipe['missedIngredientCount']}")
            r = Recepy.objects.create(
                recepy_ingredient = ingr,
                recepy_id_recepy = recipe['id'],
                recepy_title = recipe['title'],
                recepy_image = recipe['image'],
                recepy_used_ingredient_count = recipe['usedIngredientCount'],
                recepy_missed_ingredient_count = recipe['missedIngredientCount'],
            )
            print(f"Recepy {r.recepy_title} saved with used ingredient  : {r.recepy_used_ingredient_count} ,and missed ingredients: {r.recepy_missed_ingredient_count}.")
        
            print('----Recepy Ingredients...')
            print(f" --Missed Ingredients")
        except Exception as e:
                logging.error(f"Error occurred while creating Recepy: {e}")
                continue
        try:
            for ingredient_data in recipe['missedIngredients']:
            
                print(f" recepy: {r}")
                print(f" id : {ingredient_data['id']}")
                print(f" amount {ingredient_data['amount']}")
                print(f" unit : {ingredient_data['unit']}")
                print(f" name : {ingredient_data['name']}")
                print(f" meta : {ingredient_data['meta']}")
                print(f" image : {ingredient_data['image']}")

                ing = IngredientRecepy.objects.create(
                    ingrecepy_recepy=r,
                    ingrecepy_id_ingredientrecepy=ingredient_data['id'],
                    ingrecepy_amount=ingredient_data['amount'],
                    ingrecepy_unit=ingredient_data['unit'],
                    ingrecepy_name=ingredient_data['name'],
                    ingrecepy_meta=ingredient_data['meta'],
                    ingrecepy_image=ingredient_data['image'],
                    ingrecepy_is_missed=True
                )
                print(f"missedIngredient of Recepy {ing.ingrecepy_name}  saved.")
        
            print(f" --Used Ingredients")
            for ingredient_data in recipe['usedIngredients']:
                print(f" recepy: {r}")
                print(f" id : {ingredient_data['id']}")
                print(f" amount {ingredient_data['amount']}")
                print(f" unit : {ingredient_data['unit']}")
                print(f" name : {ingredient_data['name']}")
                print(f" meta : {ingredient_data['meta']}")
                print(f" image : {ingredient_data['image']}")

                IngredientRecepy.objects.create(
                    ingrecepy_recepy=r,
                    ingrecepy_id_ingredientrecepy=ingredient_data['id'],
                    ingrecepy_amount=ingredient_data['amount'],
                    ingrecepy_unit=ingredient_data['unit'],
                    ingrecepy_name=ingredient_data['name'],
                    ingrecepy_meta=ingredient_data['meta'],
                    ingrecepy_image=ingredient_data['image'],
                    ingrecepy_is_missed=False
                )
                print(f"used Ingredient of Recepy {ing.ingrecepy_name}  saved.")
        except Exception as e:
                logging.error(f"Error occurred while creating Recepy: {e}")
                continue
        print(f'Recepy saved!')
    print("\n" + "-"*40 + "\n")