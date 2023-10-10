import pandas as pd
from queries.business_info_query import get_business_info

def aggregate_business_info(api_key, businesses):
    data = []
    for business in businesses:
        try:
            info = get_business_info(business['place_id'], api_key)
            data.append({
                'Name': info['name'],
                'Type': info['type'],
                'Score': info['score'],
                'Number of Reviews': info['number_of_reviews'],
                'Comments': info['comments'],
                'latitude': info['latitude'],
                'longitude': info['longitude']
            })
        except Exception as e:
            print(f'Error: {e}')
    return pd.DataFrame(data)