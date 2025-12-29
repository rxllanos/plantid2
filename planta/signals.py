from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models, IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
import requests
from .formulas import imagefield_to_base64, headers_plant
from.api_heath import save_plant_health
from.api_ingredient import save_plant_ingredient
import json
from .models import Plant, Plant_data

@receiver(post_save, sender=Plant)
def save_plant_identification(sender, instance, created, **kwargs):
    if created:
        try:
            my_string = imagefield_to_base64(instance.plant_image)
            url_identification = "https://plant.id/api/v3/identification?details=common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,propagation_methods,watering&language=en"
            payload_identification = json.dumps({
                "images": [my_string],
                "latitude": instance.plant_latitude,
                "longitude": instance.plant_longitude,
                "similar_images": True,
            })

            response_identification = requests.post(url_identification, headers=headers_plant, data=payload_identification)
            data_plant = response_identification.json()
            plant = Plant.objects.get(plant_image=instance.plant_image)
            
            print('_____')
            print(f" access token: {data_plant['access_token']}")
            print(f" plant_binary: {data_plant['result']['is_plant']['binary']}")
            print(f" plant_probability: {data_plant['result']['is_plant']['probability']}")

            try:
                
                plant.plant_access_token = data_plant['access_token']
                plant.plant_is_plant_binary = data_plant['result']['is_plant']['binary']
                plant.plant_is_plant_probability=data_plant['result']['is_plant']['probability']
                plant.save()
                print(f"plant data saved 1st.")

            except ValidationError as e:
                print(f"Validation Error: {e.message_dict}")
            except IntegrityError as e:
                print(f"Integrity Error: {e}")
            except DatabaseError as e:
                print(f"Database Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")              

            print(f"Plant data saved.")
            print('_____')

            for dp in data_plant['result']['classification']['suggestions']:
                if dp['probability']>.8:

                    plant_instance = Plant.objects.get(pk = instance.pk)
                    print('_____')
                    print(f" Plant. details..{plant}")
                    print(f" probability: {dp['probability']}")
                    print(f" name: {dp['name']}")
                    print(f" common names: {dp['details']['common_names']}")
                    print(f" taxonmy: {dp['details']['taxonomy']['class']}")
                    print(f" url: {dp['details']['description']['citation']}")
                    print(f" gbif_id: {dp['details']['gbif_id']}")
                    print(f" inaturalist_id: {dp['details']['inaturalist_id']}")
                    print(f" image: {dp['details']['image']['value']}")
                    print(f" edible parts: {dp['details']['edible_parts']}")
                    print(f" propagation: {dp['details']['propagation_methods']}")
                    print(f" watering min: {dp['details']['watering']['min']}")
                    print(f" watering max: {dp['details']['watering']['max']}")
                    try:
                        plant_data_instance = Plant_data.objects.create(
                            plant_data_plant = plant_instance,
                            plant_data_probability = dp['probability'],
                            plant_data_name = dp['name'],
                            plant_data_common_names = dp['details']['common_names'],
                            plant_data_taxonomy = dp['details']['taxonomy']['class'],
                            plant_data_url = dp['details']['description']['citation'],
                            plant_data_gbif_id = dp['details']['gbif_id'],
                            plant_data_inaturalist_id = dp['details']['inaturalist_id'],
                            plant_data_image = dp['details']['image']['value'],
                            plant_data_edible_parts =  dp['details']['edible_parts'],
                            plant_data_propagation_methods = dp['details']['propagation_methods'],
                            plant_data_watering_min = dp['details']['watering']['min'],
                            plant_data_watering_max = dp['details']['watering']['max'],
                        )   
                        print(f"Plant details saved.")
                        save_plant_health(plant_instance)
                        save_plant_ingredient(plant_data_instance)
                    except ValidationError as e:
                        print(f"Validation Error: {e.message_dict}")
                    except IntegrityError as e:
                        print(f"Integrity Error: {e}")
                    except DatabaseError as e:
                        print(f"Database Error: {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")     

            print('_____')
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error occurred plant detail: {err}') 
        except Exception as err:
            print(f'Other error occurred plant detail: {err}')  