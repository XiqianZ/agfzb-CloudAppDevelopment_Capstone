"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.query import Query
from cloudant.error import CloudantException
from requests.auth import HTTPBasicAuth

import json
import requests

API_KEY = "fill_in_your_api_key"
URL = "fill_in_your_url"

NLP_API_KEY =  "fill_in_your_nlp_api_key"
NLP_URL = "fill_in_your_nlp_url"


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data



def cloudant_dealerships_test():
    try:
        print("start try")
        client = Cloudant.iam(None, API_KEY, url=URL, connect=True)
        db_dealerships = client["dealerships"]
        # selector = {"id": 3}
        # selector = {"id": {"$in": [1, 2, 3, 4, 5]}}
        selector = {"id": {"$gt": 0}}
        
        # selector = {'state': 'Alabama'}
        result = Query(db_dealerships, selector=selector).result
        print("===== type of Cloudant Query =====")
        for item in result:
            print(item)
            print(type(item))
            print("===========")
        # print(result)
        # print(result[0][0])
        print("===== type of Cloudant Query =====")
    
            
        print(f"Databases: {client.all_dbs()}")

    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}


def cloudant_review_db_test():
    try:
        print("Review database test")
        client = Cloudant.iam(None, API_KEY, url=URL, connect=True)
        db_reviews = client["reviews"]
        selector = {"id": {"$gt": 0}}
        result = Query(db_reviews, selector=selector).result
        print("===== type of Cloudant Query =====")
        for item in result:
            print(item)
            print(type(item))
        print("===== type of Cloudant Query =====")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}


def cloudant_review_db_post_test():
    try:
        print("Review database test")
        client = Cloudant.iam(None, API_KEY, url=URL, connect=True)
        db_reviews = client["reviews"]
        db_reviews.create_document({
            "id": 1,
            "dealership": 1,
            "name": "Johny Cage",
            "review": "I love this car",
            "purchase": True,
            "purchase_date": "2021-05-01",
            "car_make": "Audi",
            "car_model": "A4",
            "car_year": "2021"
        })
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}

def ibm_nlp_test():
    api_endpoint = "/v1/analyze?version=2022-04-07"
    api_url = f"{NLP_URL}{api_endpoint}"
    print(api_url)
    
    headers = {"Content-Type": "application/json",}
    data = {
        "html": "<html><head><title>Fruits</title></head><body><h1>Apples and Oranges</h1><p>I love apples! I don't like oranges.</p></body></html>",
        "features": {
            "emotion": {
                "targets": [
                    "apples",
                    "oranges"
                ]
            }
        }
    }
    response = requests.post(
        api_url,
        headers=headers,
        auth=("apikey", NLP_API_KEY),
        data=data,
    )
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print("Error:", response.status_code, response.text)


def analyze_review_sentiments(text):
    print("Analyzing sentiment of: " + text)
    params = {
        "version": "2021-08-01",
        "text": text,
        "features": {
            "sentiment": {}
        }
    }
    response = requests.post(NLP_URL + "/v1/analyze",
                             params=params,
                             headers={'Content-Type': 'application/json'},
                             auth=HTTPBasicAuth('apikey', NLP_API_KEY))
    json_data = json.loads(response.text)
    print(json_data)
    sentiment = json_data["sentiment"]["document"]["label"]
    print("Sentiment: " + sentiment)
    return sentiment



print("Send query to cloudant in a foreign domain")
# cloudant_dealerships_test()
# ibm_nlp_test()
# cloudant_review_db_test()
# analyze_review_sentiments("we should try another car")
# cloudant_review_db_post_test()