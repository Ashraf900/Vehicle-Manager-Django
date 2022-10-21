from django.core.validators import RegexValidator
from rest_framework.response import Response 
from rest_framework import status



'''
This validator will be used for validating the field for your Vehicle number which is alphanumeric
'''

isalphanumvalidator = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed')





#This is_admin function/decorator will check or validate if logged in user is admin or not  
def is_admin(func):
    def wrapper(request, *args):
        if request.user.is_admin==True:
            return func(request, *args)
        else:
            return Response({"Error":"Method Not Allowed"},status = status.HTTP_403_FORBIDDEN)
    return wrapper 





#This is_admin function/decorator will check or validate if logged in user is superuser or not 
def is_super(func):
    def wrapper(request, *args):
        if request.user.is_superuser==True:
            return func(request, *args)
        else:
            return Response({"Error":"Method Not Allowed"},status = status.HTTP_403_FORBIDDEN)
    return wrapper