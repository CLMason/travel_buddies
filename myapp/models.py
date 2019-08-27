from django.db import models
from datetime import datetime, timedelta
import re
import bcrypt

NOW = str(datetime.now())

class UserManager(models.Manager):
    def regValidator(self, form):
        errors = {}
        if not form['name']:
            errors['name'] = "Please enter a name."
        elif len(form['name']) < 3:
            errors['name'] = "Name must be at least three characters long."

        if not form['username']:
            errors['username'] = "Please enter a username."
        elif len(form['username']) < 3:
            errors['username'] = "Username must be at least three characters long."
        elif User.objects.filter(username=form["username"]):
            errors["username"] = "Username already exist in database. Please login"
        
        if not form['password']:
            errors['password'] = "Please enter a password."
        elif len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        
        if not form['confirm_password']:
            errors['confirm_password'] = "Please enter a confirm password."
        elif form['confirm_password'] != form['password']:
            errors['confirm_password'] = "Passwords must match."
        return errors

    def loginValidator(self, form):
        errors = {}
        if not form['username']:
            errors['username'] = "Please enter a username."
        elif len(form['username']) < 3:
            errors['username'] = "Username must be at least three characters long."
        elif not User.objects.filter(username=form["username"]):
            errors['username'] = "Username not found. Please register."
        else:
            user_list = User.objects.filter(username=form["username"])
            user = user_list[0]
            if not bcrypt.checkpw(form['password'].encode(), user.password.encode()):
                errors['password'] = "Wrong password."
            if not form['password']:
                errors['password'] = "Please enter a password."
        return errors
    
class TravelManager(models.Manager):
    def travelValidator(self, form):
        errors = {}
        if not form['destination']:
            errors['destination'] = "Please enter a destination."
        if not form["description"]:
            errors["description"] = "Please enter a description"
        if len(form['description']) < 10:
            errors['description'] = "Description must be at least ten characters long."
        if not form['travel_start']:
            errors['travel_start'] = "Please enter a travel start date."
        elif form['travel_start'] < NOW:
            errors['travel_start'] = "Travel start date cannot be in past."
        if not form['travel_end']:
            errors["travel_end"] = "Please enter an travel end date."
        elif form["travel_end"] < form['travel_start']:
            errors['travel_end'] = "End date cannot be before start date."
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Travel(models.Model):
    added_by = models.ForeignKey(User, related_name="trip_added", on_delete=models.CASCADE) 
    destination = models.CharField(max_length=255)
    plan = models.TextField()
    travel_start = models.DateTimeField()
    travel_end = models.DateTimeField()
    users_trips = models.ManyToManyField(User, related_name="user_schedules")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TravelManager()