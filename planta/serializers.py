from rest_framework import serializers
from .models import (Plant, Plant_data, HealthAssessment,DiseaseSuggestion, 
    Ingredient, NutrientDetail, Property, Flavonoid, CaloricBreakdown, 
    WeightPerServing, Recepy, IngredientRecepy
)

import json


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__' 

class PlantDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant_data
        fields = '__all__' 

class HealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthAssessment
        fields = '__all__' 

class DeseaseSuggestionSerializer(serializers.ModelSerializer):        

    def to_representation(self, instance):
            data = super().to_representation(instance)

            fields_to_clean = [
                "disease_treatment_chemical", 
                "disease_treatment_biological", 
                "disease_prevention", 
                "disease_common_names_disease"
            ]

            for field in fields_to_clean:
                if isinstance(data.get(field), str):
                    try:
                        # Remove '/' and replace single quotes for valid JSON
                        cleaned_string = data[field].replace("/", "").replace("'", '"')
                        parsed_data = json.loads(cleaned_string)

                        # Ensure parsed_data is a list
                        if isinstance(parsed_data, str):
                            data[field] = [parsed_data]
                        elif isinstance(parsed_data, list):
                            # Remove '/' from each string in the list
                            data[field] = [item.replace("/", "") if isinstance(item, str) else item for item in parsed_data]
                        else:
                            data[field] = [str(parsed_data)]

                    except json.JSONDecodeError:
                        # If JSON parsing fails, fallback to list with cleaned string
                        data[field] = [data[field].replace("/", "")]

                elif isinstance(data.get(field), list):
                    # Ensure strings inside lists are cleaned
                    data[field] = [item.replace("/", "") if isinstance(item, str) else item for item in data[field]]

            return data      

    class Meta:
        model = DiseaseSuggestion
        fields = '__all__' 

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__' 

class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutrientDetail
        fields = '__all__' 

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__' 


class FlavonoidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavonoid
        fields = '__all__' 


class CaloricBreakdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaloricBreakdown
        fields = '__all__' 


class WeightPerServingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightPerServing
        fields = '__all__' 


class RecepySerializer(serializers.ModelSerializer):
    class Meta:
        model = Recepy
        fields = '__all__' 


class IngredientRecepySerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientRecepy
        fields = '__all__' 

class CombinedSerializer(serializers.ModelSerializer):
    Plant = PlantSerializer()
    Plant_data = PlantDataSerializer()
    HealthAssessment = HealthSerializer()
    DiseaseSuggestion = DeseaseSuggestionSerializer()
    Ingredient = IngredientSerializer()
    NutrientDetail = NutrientSerializer()
    Property = PropertySerializer()
    Flavonoid = FlavonoidSerializer()
    CaloricBreakdown = CaloricBreakdownSerializer()
    WeightPerServing = WeightPerServingSerializer()
    Recepy = RecepySerializer()
    IngredientRecepy = IngredientRecepySerializer()

    class Meta:
        model = Plant
        fields = '__all__'