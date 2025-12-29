from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
import requests
from .formulas import imagefield_to_base64, save_plant_desease, headers_plant
import json
from .models import HealthAssessment

def save_plant_health(plant_instance):
    try:
        my_string = imagefield_to_base64(plant_instance.plant_image)
        url_health = 'https://plant.id/api/v3/health_assessment?details=local_names,description,url,treatment,common_names,cause&language=en'
        payload_health = json.dumps({
        "images": [my_string],
        "latitude": plant_instance.plant_latitude,
        "longitude": plant_instance.plant_longitude,
        "similar_images": True,
        })

        response_health = requests.post(url_health, headers=headers_plant, data=payload_health)
        data_health = response_health.json()  
        print('_____')
        print(f" Health...{plant_instance}")
        try:
            health_instance = HealthAssessment.objects.create(
                health_plant = plant_instance,
                health_is_healthy_binary= data_health['result']['is_healthy']['binary'],
                health_is_healthy_probability= data_health['result']['is_healthy']['probability'],      
            )    

            print(f"health {plant_instance} saved.")    
            print(f"Health assestment :  {health_instance.health_is_healthy_binary}")
        except ValidationError as e:
            print(f"Validation Error: {e.message_dict}")
        except IntegrityError as e:
            print(f"Integrity Error: {e}")
        except DatabaseError as e:
            print(f"Database Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")        
        print('_____')
        if not health_instance.health_is_healthy_binary: 
            save_plant_desease(health_instance,data_health)

    except requests.exceptions.HTTPError as err:
        print(f'HTTP error occurred in health assestment: {err}') 
    except Exception as err:
        print(f'Other error occurred in health assestment: {err}')   