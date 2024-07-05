import requests

# Replace with your Unsplash API access key
ACCESS_KEY = 'Q0rd3GyW2Ps2N8RjcrVyuNO0riZpxUKaZeBI4mNTz7g'

# Endpoint for searching photos
endpoint = 'https://api.unsplash.com/search/photos'

# Query parameters
query_params = {
    'query': 'nature',  # Replace with your search query
    'client_id': ACCESS_KEY
}

# Make a GET request to Unsplash API
response = requests.get(endpoint, params=query_params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse JSON response
    data = response.json()
    # Extract URLs of the first 5 photos from the response
    for photo in data['results'][:5]:
        print(photo['urls']['regular'])
else:
    print('Failed to retrieve data:', response.status_code)
