from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Event, Registration
from api.serializer import UserRegisterSerializer, EventSerializer, EventRegisterSerializer, ReportSerializer
from django.contrib.auth import authenticate
from utils.permissions import JWTToken
from utils.permissions import CustamizePermission


# Create your views here.
class UserRegisterAPI(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                data={"response": 'user created successfully'},
                status=status.HTTP_201_CREATED
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


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
                status=status.HTTP_404_NOT_FOUND
            )


class EventAPI(APIView):
    def get(self, request, id=None):
        if id:
            event_queryset = Event.objects.filter(id=id).first()

            if not event_queryset:
                return Response(
                    data={"error": "invalid event id"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = EventSerializer(event_queryset, many=False)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        event_queryset = Event.objects.all()

        serializer = EventSerializer(event_queryset, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            response_object = serializer.save()
            return Response(
                data={"response": f'{response_object.title} Created Successfully'},
                status=status.HTTP_200_OK
            )
        return Response(data=serializer.errors)

    def patch(self, request, id):

        event_queryset = Event.objects.filter(id=id).first()

        if not event_queryset:
            return Response(
                data={"error": 'event not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EventSerializer(event_queryset, data=request.data, partial=True)
        if serializer.is_valid():
            response_object = serializer.save()
            return Response(
                data={"success": f'{response_object.title} edited successfully'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        event_queryset = Event.objects.filter(id=id).first()

        if not event_queryset:
            return Response(
                data={"error": "event not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        event_queryset.delete()
        return Response(
            data={"success": "Event deleted successfully"},
            status=status.HTTP_200_OK
        )


class EventRegisterAPI(APIView):
    def post(self, request):
        serializer = EventRegisterSerializer(data=request.data)
        if serializer.is_valid():
            response_object = serializer.save()
            return Response(
                data={"success": f"registration to {response_object.event.title} successfull"},
                status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ReportAPI(APIView):

    def get(self, request):

        registration_queryset = Registration.objects.all()
        serializer = ReportSerializer(registration_queryset, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class CountEventsAPI(APIView):
    def get(self, request):
        registration_count = Registration.objects.count()
        event_count = Event.objects.count()
        return Response(
            data={
                "registration_count": registration_count,
                "event_count": event_count
                  },
            status=status.HTTP_200_OK
        )

