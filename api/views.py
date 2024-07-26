from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializer import UserRegisterSerializer
from django.contrib.auth import authenticate
from utils.permissions import JWTToken


# Create your views here.
class UserRegisterAPI(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                data={'user created successfully'},
                status=status.HTTP_201_CREATED
            )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None:
            return Response(
                data={"please enter your username"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password is None:
            return Response(
                data={'please enter your password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user:
            token = JWTToken().generate(user)
            return Response(
                data=token,
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                data={'invalid username or password'},
                status=status.HTTP_400_BAD_REQUEST
            )