import requests
from facebook.data.api_utils import load_prediction_api_vars

def covid_stats(posts):
    prediction_url = load_prediction_api_vars()
    params = posts[["id", "message"]]
    response = requests.post(prediction_url, params=params)
    return response
