from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate

from . serializers import UserSerializer, RegistrationSerializer,ProfileSerializer
from . models import Profile
from .utils import logMail
# REGISTER USER
class RegistrationView(APIView):
    def post(self,request):
        try:
            serializers =RegistrationSerializer(data= request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# LOGIN USER
class LoginView(APIView):
    def post(self,request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                logMail(username,user.email)
                login(request,user)
                return Response({"message":f"{username} Login successful"}, status=status.HTTP_200_OK)
            return Response({"message":"Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# LOGOUT USER
class LogoutView(APIView):
    def post(self,request):
        try:
           logout(request)
           return Response({"message":f"logged out successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)