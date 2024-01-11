from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel, DealerReview
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

#Cloudant
from cloudant.client import Cloudant
from cloudant.query import Query

#std
from datetime import datetime
import logging
import json
from . import restapis

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create an `about` view to render a static about page
def about(request):
    context = {}

    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

def logout_request(request):
    context = {}
    logout(request)
    return render(request, 'djangoapp/index.html', context)


def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        username = request.POST['uid']
        password = request.POST['pwd']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        user_exist = False
        try:
            user = User.objects.get(username = username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Index and detail dealerships views
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        dealerships = restapis.get_all_dealers_from_cf()
        dealer_names = [dealer.short_name for dealer in dealerships]
        context["dealer_names"] = dealer_names
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        if(dealer_id):
            print(f"==== get_dealer_details, input: dealer_id {dealer_id}")
            dealer = restapis.get_dealer_from_cf_by_id(dealer_id)
            reviews = restapis.get_review_by_dealer_id_from_cf(dealer_id)
            context["dealer"] = dealer
            context["reviews"] = reviews
            return render(request, 'djangoapp/dealer_details.html', context)
        else:
            return redirect("djangoapp:index")



# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    print(f"==== add_review, input: dealer_id {dealer_id}")
    #Check authentication
    if not request.user.is_authenticated:
        return redirect("djangoapp:index")
    else:
        context = {}
        if request.method == "GET":
            dealer = restapis.get_dealer_from_cf_by_id(dealer_id)
            cars = CarModel.objects.filter(dealer_id=dealer_id)
            context["dealer"] = dealer
            context["cars"] = cars
            return render(request, 'djangoapp/add_review.html', context)
        elif request.method == "POST":
            carModel_instance = get_object_or_404(CarModel, pk=request.POST['car'])
            purchase_date_str = datetime.strptime(request.POST['purchase_date'], '%m/%d/%Y')
            formatted_date_str = purchase_date_str.strftime('%Y-%m-%d')
            
            payload = DealerReview(
                id = request.user.id,
                dealership = dealer_id,
                name = request.user.first_name + " " + request.user.last_name,
                purchase = request.POST['purchasecheck'],
                review = request.POST['review_content'],
                purchase_date = formatted_date_str,
                car_make = carModel_instance.maker.name,
                car_model = carModel_instance.name,
                car_year = carModel_instance.year.strftime("%Y"),
                sentiment="",
            )
            try:              
                if(restapis.add_review_to_db(payload)):
                    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
            except:
                logger.error("Unable to connect to Cloudant")
            finally:
                return redirect("djangoapp:add_review", dealer_id=dealer_id)