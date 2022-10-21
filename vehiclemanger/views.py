from rest_framework.response import Response 
from rest_framework import status
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from vehiclemanger.models import VehiclesTab
from .serializers import UserLoginSerializer,  UserRegistrationSerializer, VehiclesSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .validators import is_admin, is_super



'''
Generating Token manually with below function
'''
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistrationView(APIView):
    '''
    Created this class based view to register new users similarly we can perform all CRUD Operation.
    '''
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception =True):
            user = serializer.save()
            return Response({"msg":"successful user register"},status = status.HTTP_201_CREATED) 
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)







class UserLoginView(APIView):
    '''
    This class is providing login service to user and giving out the token for further actions
    '''
    def post(self, request, format=None):
        serializer =UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email =email, password=password)
            token = get_tokens_for_user(user)
            if user is not None:
                return Response({'token':token, 'msg':'Success login'}, status =status.HTTP_200_OK)
            else:
                return Response ({'errors':{'non_field_errors':['Email or password is not Valid']}}, status= status.HTTP_404_NOT_FOUND)

class VehicleManager(APIView):
    '''
    In this class we have three different requirements for performing CRUD in vehicles table i.e. VehicleTab
    case1: super user or super admin can perform CRUD operation
    case2: admin or staff can only perform RU operation
    case3: normal user can only perform Read operation
    '''
    @method_decorator(is_super)
    def post(self, request):
        serializer = VehiclesSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg":"Successfully vehicle registered"}, status =status.HTTP_201_CREATED)
        else:
            return Response({"Error":"invalid request"}, status = status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        vehicles = VehiclesTab.objects.all()
        serializer = VehiclesSerializer(vehicles, many=True)
        return Response({"vehicles":serializer.data})
    
    @method_decorator(is_admin)
    def put(self,request):
        vehicle_numb = request.data.get('vehicle_number')
        vehicle = VehiclesTab.objects.get(vehicle_number = vehicle_numb)
        serializer = VehiclesSerializer(vehicle, data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg":"Succefull vehicle detail updated"}, status = status.HTTP_200_OK)
        else:
            return Response({"Error":"Invalide request"}, status = status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(is_super)
    def delete(self, request):
        vehicle_numb = request.data.get('vehicle_number')
        vehicle = VehiclesTab.objects.get(vehicle_number = vehicle_numb)
        if vehicle is not None:
            vehicle.delete()
            return Response({"msg":"vehicle removed successfully"}, status = status.HTTP_200_OK)
        else:
            return Response({"Erro":"Erro has occured"},status = status.HTTP_400_BAD_REQUEST)