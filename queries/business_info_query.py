import requests
import json

def get_business_info(place_id, api_key):
    endpoint_url = f"https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={api_key}"
    response = requests.get(endpoint_url)
    response_json = response.json()

    if response.status_code == 200 and response_json.get('result'):
        result = response_json['result']
        return {
            'name': result.get('name'),
            'type': result.get('types')[0] if result.get('types') else None,
            'score': result.get('rating'),
            'number_of_reviews': result.get('user_ratings_total'),
            'comments': [review['text'] for review in result.get('reviews', [])[:20]],
            'geometry': result.get('geometry'),
            'latitude': result['geometry']['location']['lat'],
            'longitude': result['geometry']['location']['lng']
            # ... any other information you need
        }
    else:
        raise Exception(f'Failed to retrieve business info: {response_json}')