from django.db import models
from accounts.models import CustomUser

class Plant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="user")
    plant_access_token = models.CharField(default=0000, max_length=255)
    plant_is_plant_binary = models.BooleanField(default=True)
    plant_is_plant_probability = models.FloatField(default=1)
    plant_image = models.ImageField(default=None, upload_to='images/')
    plant_latitude = models.FloatField(default=4.787029680509281, blank=True)
    plant_longitude = models.FloatField(default=-74.15851704555615, blank=True)

    def __str__(self):
        return f"Plant id : {self.plant_access_token}, is a plant? {self.plant_is_plant_binary} "
    
class Plant_data(models.Model):
    plant_data_plant = models.OneToOneField(Plant, on_delete=models.CASCADE)
    plant_data_probability = models.FloatField(default= 0)
    plant_data_name = models.CharField(default=0000, max_length=255)
    plant_data_common_names = models.TextField(default='', blank=True)
    plant_data_url = models.URLField(default=None, blank=True)
    plant_data_taxonomy = models.TextField(default='', blank=True)
    plant_data_gbif_id = models.IntegerField(default=0, blank=True)
    plant_data_inaturalist_id = models.IntegerField(default='', blank=True)
    plant_data_image = models.URLField(default=None, blank=True)
    plant_data_edible_parts = models.TextField(default='', blank=True)
    plant_data_propagation_methods = models.TextField(default='', blank=True)
    plant_data_watering_min = models.IntegerField(default=0, blank=True)
    plant_data_watering_max = models.IntegerField(default=0, blank=True)
    def __str__(self):
        return f"Scientific name: {self.plant_data_name}, id = {self.plant_data_gbif_id}, eatable? {self.plant_data_edible_parts}"
    
class HealthAssessment(models.Model):
    health_plant = models.OneToOneField(Plant, on_delete=models.CASCADE)
    health_is_healthy_binary = models.BooleanField(default=True)
    health_is_healthy_probability = models.FloatField(default=1)
    def __str__(self):
        return f"Plant: {self.health_plant.plant_access_token} , Is healthy {self.health_is_healthy_binary}"

class DiseaseSuggestion(models.Model):
    disease_health_assessment = models.ForeignKey(HealthAssessment, on_delete=models.CASCADE)
    disease_id_DiseaseSuggestion = models.CharField(default='', blank=True)
    disease_name = models.CharField(default='', blank=True)
    disease_probability = models.FloatField(default=0, blank=True)
    disease_description = models.TextField(default='', blank=True)
    disease_url = models.URLField(default=None, blank=True)
    disease_treatment_chemical = models.CharField(blank=True, null=True,)
    disease_treatment_biological = models.CharField(blank=True, null=True,)
    disease_prevention = models.CharField(default=dict, null=True, blank=True)
    disease_common_names_disease = models.CharField(default='', null=True, blank=True)
    disease_cause = models.CharField(default='', null=True, blank=True)    
    def __str__(self):
        return f"Desease: {self.disease_name}"

class IngredientID(models.Model):
    spoon_name = models.CharField(max_length=255)
    spoon_id_ingredients = models.IntegerField(primary_key=True)    
    def __str__(self):
        return f"Name: {self.spoon_name} - ID: ({self.spoon_id_ingredients})"


class Ingredient(models.Model):
    ingredient_plant = models.ForeignKey(Plant_data, on_delete=models.CASCADE, default='')
    ingredient_id_Ingredient = models.IntegerField(default=0)
    ingredient_original_name = models.CharField(default='', max_length=255, blank=True)
    ingredient_amount = models.FloatField(default=0, blank=True, null=True)
    ingredient_unit = models.CharField(default='', max_length=255, blank=True)
    ingredient_possible_units = models.CharField(default='', blank=True, null=True)
    ingredient_estimated_cost_value = models.FloatField(default=0, blank=True)
    ingredient_estimated_cost_unit = models.CharField(default='', max_length=255, blank=True)
    ingredient_consistency = models.CharField(default='', max_length=255, blank=True, null=True)
    ingredient_img = models.ImageField(default='', upload_to='images/', blank=True)
    def __str__(self):
        return f"Ingredient Name : {self.ingredient_original_name}, Amount: {self.ingredient_amount} Unit: {self.ingredient_unit} Cost: {self.ingredient_estimated_cost_unit}"


class NutrientDetail(models.Model):
    nutrient_ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, default='')
    nutrient_name = models.CharField(default='', max_length=255, blank=True)
    nutrient_amount = models.FloatField(default=0, blank=True)
    nutrient_unit = models.CharField(default='', max_length=255, blank=True)
    nutrient_percent_of_daily_needs = models.FloatField(default=0, blank=True)
    def __str__(self):
        return f"Nutrient Name : {self.nutrient_name}, Amount: {self.nutrient_amount} Unit: {self.nutrient_unit} % Daily Need: {self.nutrient_percent_of_daily_needs}"

class Property(models.Model):
    property_ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, default='')
    property_name = models.CharField(default='', max_length=255, blank=True)
    property_amount = models.FloatField(default=0, blank=True)
    property_unit = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return f"Property Name : {self.property_name}, Amount: {self.property_amount} Unit: {self.property_unit}."

class Flavonoid(models.Model):
    flavonoid_ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, default='')
    flavonoid_name = models.CharField(default='', max_length=255, blank=True)
    flavonoid_amount = models.FloatField(default=0, blank=True)
    flavonoid_unit = models.CharField(default='', max_length=255, blank=True)
    def __str__(self):
        return f"Flavonoid Name : {self.flavonoid_name}, Amount: {self.flavonoid_amount} Unit: {self.flavonoid_unit}."

class CaloricBreakdown(models.Model):
    cb_ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    cb_percent_protein = models.FloatField(default=0, blank=True)
    cb_percent_fat = models.FloatField(default=0, blank=True)
    cb_percent_carbs = models.FloatField(default=0, blank=True)
    def __str__(self):
        return f"Protein : {self.cb_percent_protein}, Fat: {self.cb_percent_fat} Carbs: {self.cb_percent_carbs}."

class WeightPerServing(models.Model):
    wps_ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    wps_amount = models.FloatField(default=0, blank=True)
    wps_unit = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return f" WPS amount : {self.wps_amount}, unit: {self.wps_unit}."

class Recepy(models.Model):
    recepy_ingredient = models.ForeignKey(Ingredient, default=0000, on_delete=models.CASCADE)
    recepy_id_recepy = models.IntegerField(default=0, blank=True)
    recepy_title = models.CharField(max_length=200, blank=True)
    recepy_image = models.URLField(blank=True)
    recepy_used_ingredient_count = models.IntegerField(blank=True)
    recepy_missed_ingredient_count = models.IntegerField(blank=True)
    def __str__(self):
        return f"Title : {self.recepy_title}, Used Ingredient: {self.recepy_used_ingredient_count} Missed Ing: {self.recepy_missed_ingredient_count}."


class IngredientRecepy(models.Model):
    ingrecepy_recepy = models.ForeignKey(Recepy, on_delete=models.CASCADE)
    ingrecepy_id_ingredientrecepy = models.IntegerField()
    ingrecepy_amount = models.FloatField(blank=True)
    ingrecepy_unit = models.CharField(max_length=255, blank=True)
    ingrecepy_name = models.CharField(max_length=255, blank=True)
    ingrecepy_meta = models.CharField(max_length=255, blank=True)
    ingrecepy_image = models.ImageField(upload_to='images/', blank=True)
    ingrecepy_is_missed = models.BooleanField(default=False, blank=True)
    def __str__(self):
        return f"Ingredient : {self.ingrecepy_recepy.recepy_title} , Name : {self.ingrecepy_name}, Missed : {self.ingrecepy_is_missed}, Unit {self.ingrecepy_unit} Amount: {self.ingrecepy_amount}."










