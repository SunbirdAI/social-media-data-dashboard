import requests

from twitter.data_layer.api.api_utils import load_env_vars, create_headers, create_url_with_query, create_query


def connect_to_endpoint(url: str, headers: str):
    """
    Makes an http request to the given url with the given headers
    :param url: url to request
    :param headers: auth headers
    :return: the response from the request
    """
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        print("No more results: Status code: {} Response: {}".format(response.status_code, response.text))
        return {"data": [], "meta": {}}, response.status_code
    return response.json(), response.status_code


def fetch_tweets(mode="moh"):
    env_vars = load_env_vars()
    api_root = env_vars["api_root"]
    bearer_token = env_vars["token"]
    # TODO: Get users from db when that's added
    query = create_query(["MinofHealthUG", "JaneRuth_Aceng", "WHOUganda"])
    url = create_url_with_query(api_root, query)
    headers = create_headers(bearer_token)

    tweets = []
    json_response, status_code = connect_to_endpoint(url, headers)

    while True:
        if "data" in json_response:
            tweets.extend(json_response["data"])

        if "meta" in json_response and "next_token" in json_response["meta"]:
            new_url = url + "&next_token={}".format(json_response["meta"]["next_token"])
            json_response, status_code = connect_to_endpoint(new_url, headers)
        else:
            break

    return tweets, status_code
