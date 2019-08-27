from django.urls import path
from myapp import views


urlpatterns = [
path('', views.index),
path('main', views.main),
path('register', views.register),
path('login', views.login),
path('travels',views.travels),
path('travels/add', views.add_trip),
path('create_trip', views.create_trip),
path('travels/destination/<id>',views.display),
path('join_trip/<travel_id>', views.join_trip),
path('logout',views.logout),
]