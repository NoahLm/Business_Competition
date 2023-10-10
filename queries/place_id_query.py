# queries/place_id_query.py
import requests
import json

def get_place_id(business_name, latitude, longitude, api_key):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        'input': business_name,
        'inputtype': 'textquery',
        'locationbias': f'point:{latitude},{longitude}',
        'fields': 'place_id',
        'key': api_key
    }

    response = requests.get(endpoint_url, params=params)
    response_json = response.json()

    if response.status_code == 200 and response_json.get('candidates'):
        return response_json['candidates'][0]['place_id']
    else:
        raise Exception(f'Failed to retrieve Place ID: {response_json}')
