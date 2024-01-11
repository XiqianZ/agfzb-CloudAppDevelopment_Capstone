from . import models
import requests
import json
from requests.auth import HTTPBasicAuth
from cloudant.client import Cloudant
from cloudant.query import Query
from cloudant.error import CloudantException



# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

API_KEY = "rPnaY-vOBNNyYso8OV8I-blbzPLVEVC4cav9HJu_KanU"
URL = "https://2fb1c265-3843-44c8-ab91-5a01d1e387b8-bluemix.cloudantnosqldb.appdomain.cloud"


NLP_API_KEY =  "e9BlgpP9SCT0BCAEk8F0504YEUg7wqh-JP3yW_QDHBtS"
NLP_URL = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/c39bd6e1-e50c-4ebd-9413-b7a7c0dad472"


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if kwargs is not None:
            print("GET with params: {}".format(kwargs))
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'})
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
    


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dearler_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    dealers = json_result["rows"]
    print(dealers)
    return results

def get_dealer_from_cf_by_id(id):
    client = Cloudant.iam(None, API_KEY, url=URL, connect=True)
    db_dealerships = client["dealerships"]
    selector = {"id": id}
    try:
        result = Query(db_dealerships, selector=selector).result
        if result:
            dealer = models.CarDealer(
                address=result[0][0]["address"],
                city=result[0][0]["city"],
                full_name=result[0][0]["full_name"],
                id=result[0][0]["id"],
                lat=result[0][0]["lat"],
                long=result[0][0]["long"],
                short_name=result[0][0]["short_name"],
                state=result[0][0]["state"],
                st=result[0][0]["st"],
                zip=result[0][0]["zip"]
            )
            return dealer
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

def get_all_dealers_from_cf():
    all_dealers = []
    client = Cloudant.iam(None, API_KEY, url=URL, connect=True)
    db_dealerships = client["dealerships"]
    selector = {"id": {"$gt": 0}}
    try:
        result = Query(db_dealerships, selector=selector).result
        if result:
            for dealer in result:
                dealer_obj = models.CarDealer(
                    address=dealer["address"],
                    city=dealer["city"],
                    full_name=dealer["full_name"],
                    id=dealer["id"],
                    lat=dealer["lat"],
                    long=dealer["long"],
                    short_name=dealer["short_name"],
                    state=dealer["state"],
                    st=dealer["st"],
                    zip=dealer["zip"]
                )
                all_dealers.append(dealer_obj)
            return all_dealers
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_review_by_dealer_id_from_cf(dealership_Id):
    dealer_reviews = []  
    client = Cloudant.iam(None, API_KEY, url=URL, connect=True)
    db_reviews = client["reviews"]
    selector = {"dealership": dealership_Id}
    result = Query(db_reviews, selector=selector).result
    if result:
        for review in result:
            if review["purchase"]:
                dealer_review = models.DealerReview(
                    dealership=review["dealership"],
                    name=review["name"],
                    purchase=review["purchase"],
                    review=review["review"],
                    id=review["id"],
                    sentiment=analyze_review_sentiments(review["review"]),
                    purchase_date = review["purchase_date"],
                    car_make = review["car_make"],
                    car_model = review["car_model"],
                    car_year = review["car_year"],
                )
            else:
                dealer_review = models.DealerReview(
                    dealership=review["dealership"],
                    name=review["name"],
                    purchase=review["purchase"],
                    review=review["review"],
                    id=review["id"],
                    sentiment=analyze_review_sentiments(review["review"]),
                    purchase_date = " ",
                    car_make = " ",
                    car_model = " ",
                    car_year = " ",
                )
            dealer_reviews.append(dealer_review)
    return dealer_reviews
 

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
    # print(json_data)
    sentiment = json_data["sentiment"]["document"]["label"]
    # print("Sentiment: " + sentiment)
    return sentiment

def add_review_to_db(review):
    client = Cloudant.iam(None, API_KEY, url=URL, connect=True)
    db_reviews = client["reviews"]
    print(f"==== add_review_to_db, input: {review.id} {review.dealership} {review.name} {review.purchase} {review.review} {review.purchase_date} {review.car_make} {review.car_model} {review.car_year}")
    try:
        db_reviews.create_document({
            "id": review.id,
            "dealership": review.dealership,
            "name": review.name,
            "purchase": review.purchase,
            "review": review.review,
            "purchase_date": review.purchase_date,
            "car_make": review.car_make,
            "car_model": review.car_model,
            "car_year": review.car_year,
        })
        return True
    except CloudantException as cloudant_exception:
        print(f"unable to add {cloudant_exception.__str__()}")
        return False

