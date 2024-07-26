from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializer import UserRegisterSerializer


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
