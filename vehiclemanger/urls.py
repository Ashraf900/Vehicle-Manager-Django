from django.urls import path
from .views import UserRegistrationView, UserLoginView, VehicleManager 
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('vehicles/', VehicleManager.as_view(),name= 'vehicles')
]