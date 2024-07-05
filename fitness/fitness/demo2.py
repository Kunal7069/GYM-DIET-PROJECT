import requests

ACCESS_KEY = 'Q0rd3GyW2Ps2N8RjcrVyuNO0riZpxUKaZeBI4mNTz7g'
endpoint = 'https://api.unsplash.com/search/photos'
query_params = {
    'query': 'nature',  
    'client_id': ACCESS_KEY
}
response = requests.get(endpoint, params=query_params)
if response.status_code == 200:
    data = response.json()
    for photo in data['results'][:1]:
        print(photo['urls']['regular'])
else:
    print('Failed to retrieve data:', response.status_code)
