import requests
import json

def search_competing_businesses(api_key, business_type, latitude, longitude, radius):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'type': business_type,
        'key': api_key
    }
    
    response = requests.get(endpoint_url, params=params)
    
    if response.status_code == 200:
        result = response.json()
        return result['results']
    else:
        raise Exception(f'Failed to retrieve data: {response.content}')