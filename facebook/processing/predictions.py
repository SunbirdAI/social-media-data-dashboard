import requests
from facebook.data.api_utils import load_prediction_api_vars


def covid_predictions(posts):
    prediction_url = load_prediction_api_vars()
    posts_for_prediction = posts[["id", "message"]]
    posts_for_prediction.rename(
        columns={"message": "text"},
        inplace=True
    )
    posts_for_prediction["id"] = posts_for_prediction["id"].astype(str)
    posts_for_prediction["text"] = posts_for_prediction["text"].astype(str)
    params = {"text_list": posts_for_prediction.to_dict("records")}
    response = requests.post(prediction_url, json=params)
    return response.json()
