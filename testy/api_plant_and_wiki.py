import requests
import base64
import json
import wikipediaapi


url = "https://plant.id/api/v3/identification?details=common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,propagation_methods,watering&language=en"
api_key= 'zUy9E42cGnlpS4hvJuENyDFClzxGVvmbe5H31VGIkIFNq0QOoi'

with open("plantas/Images/Image.jpg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read()).decode('utf-8')

# payload = json.dumps({
#   "images": [my_string],
#   "latitude": 4.7869869042783595,
#   "longitude": -74.15857071004574,
#   "similar_images": True,
# })

headers = {
  'Api-Key': api_key,
  'Content-Type': 'application/json'
}

# response = requests.post(url, headers=headers, data=payload)
# data = response.json()
# print(response.status_code)
# print(response.url)
# print(dir(response))

url2 = 'https://plant.id/api/v3/health_assessment?details=local_names,description,url,treatment,common_names,cause&language=en'
payload2 = json.dumps({
  "images": [my_string],
  "latitude": 4.7869869042783595,
  "longitude": -74.15857071004574,
  "similar_images": True,
})
response2 = requests.post(url2, headers=headers, data=payload2)
data2 = response2.json()
print(response2.status_code)
print(response2.url)
print(dir(response2))
print(data2['result']['is_plant']['binary'])
print(data2['result']['is_healthy']['binary'])
print(type(data2['result']['is_plant']['binary']))
print(type(data2['result']['is_healthy']['binary']))
print(data2['result']['is_plant']['binary'] and not data2['result']['is_healthy']['binary'])


# wiki = wikipediaapi.Wikipedia('rxllanos@gmail.com/1.0','en')
# page = wiki.page('Dracaena fragrans')
# print("Page - Exists: %s" % page.exists())

# print(dir([page]))


# data3 = {
#     'title': page.title,
#     'summary': page.summary,
#     'sections': []
# }

# for section in page.sections:
#     data3['sections'].append({
#         'title': section.title,
#         'text': section.text
#     })
# json_data = json.dumps(data3, indent=4)


with open('apiresponse.json', 'w') as json_file:
    json.dump([data2], json_file)


# identification = response.json()
# print('is plant' if identification['result']['is_plant']['binary'] else 'is not plant')
# for suggestion in identification['result']['classification']['suggestions']:
#     print(suggestion['name'])
#     print(f'probability {suggestion["probability"]:.2%}')
#     print(suggestion['details']['url'], suggestion['details']['common_names'])
#     print()





