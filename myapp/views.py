from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
    return redirect('/main')

def main(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.regValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(name=request.POST["name"], username=request.POST["username"], password=hashed_pw.decode())

        request.session['id'] = new_user.id
        return redirect('/travels')

def login(request):
    errors = User.objects.loginValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    else:
        user_list = User.objects.filter(username=request.POST['username'])
        user = user_list[0]
        request.session['id'] = user.id
        return redirect('/travels')

def travels(request):
    if 'id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session["id"]) #getting the user in session
        all_trips = Travel.objects.all()
        user_schedule = user.user_schedules.all()
        other_users = all_trips.difference(user_schedule)
        context = {
            'user' : user,
            'user_schedule': user_schedule,
            'other_users': other_users,
        }
    return render(request, "travels.html", context)

def add_trip(request):
    if 'id' not in request.session:
        return redirect("/")
    else:
        return render(request,'add_trip.html')

def create_trip(request):
    errors = Travel.objects.travelValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/travels/add')
    else:
        user = User.objects.get(id=request.session["id"])
        trip = Travel.objects.create(destination=request.POST["destination"], plan=request.POST["description"], travel_start=request.POST['travel_start'], travel_end=request.POST['travel_end'],added_by_id=request.session['id'])
        user.user_schedules.add(trip)
    return redirect("/travels")

def display(request,id):
    if 'id' not in request.session:
            return redirect("/")
    else:
        trip = Travel.objects.get(id=id)
        user = User.objects.get(id=request.session["id"])
        users_who_join = trip.users_trips.exclude(id=trip.added_by_id)

        context = {
            "trip": trip,
            "user": user,
            "users": users_who_join
        }
    return render(request, "show_destination.html", context)

def join_trip(request, travel_id):
    if 'id' not in request.session:
            return redirect("/")
    else:
        user = User.objects.get(id=request.session["id"])
        trip = Travel.objects.get(id=travel_id)
        user.user_schedules.add(trip)
        return redirect("/travels")


def logout(request):
    request.session.clear()
    return redirect("/")