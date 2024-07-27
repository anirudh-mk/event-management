from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Event, Registration
from api.serializer import UserRegisterSerializer, EventSerializer, EventRegisterSerializer, ReportSerializer
from django.contrib.auth import authenticate

from utils.decorator import role_required
from utils.permissions import JWTToken
from utils.permissions import CustamizePermission
from .signals import notification_signal, update_notification_signal


class UserRegisterAPI(APIView):
    """
     API view to handle user registration.
     """
    def post(self, request):
        # pass data to serializer
        serializer = UserRegisterSerializer(data=request.data)
        # check the serializer object is valid
        if serializer.is_valid():
            serializer.save()
            # if serializer is valid return success response
            return Response(
                data={"success": 'user created successfully'},
                status=status.HTTP_201_CREATED
            )
        # if serializer object is not valid return serializer errors
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLoginAPI(APIView):
    """
         API view to handle user registration.
         """
    def post(self, request):
        # fetch username and password from the body
        username = request.data.get('username')
        password = request.data.get('password')

        # check username is none or not if none return failure response
        if username is None:
            return Response(
                data={"error": "please enter your username"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # check password is none or not if none return failure response
        if password is None:
            return Response(
                data={"error": 'please enter your password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # authenticate user with username and password
        user = authenticate(username=username, password=password)

        # check wether the user exists or not
        if user:
            # if user exists generate jwt token with username and send token in response
            token = JWTToken().generate(user)
            return Response(
                data=token,
                status=status.HTTP_200_OK
            )
        # if  user not exists return error response
        else:
            return Response(
                data={'error': 'invalid username or password'},
                status=status.HTTP_404_NOT_FOUND
            )


class EventAPI(APIView):
    authentication_classes = [CustamizePermission]

    @role_required(['admin', 'organizer'])
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

    @role_required(['admin'])
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            response_object = serializer.save()

            notification_signal.send(sender=response_object.__class__, instance=response_object)

            return Response(
                data={"response": f'{response_object.title} Created Successfully'},
                status=status.HTTP_200_OK
            )
        return Response(data=serializer.errors)

    @role_required(['admin'])
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
            update_notification_signal.send(sender=response_object.__class__, instance=response_object)
            return Response(
                data={"success": f'{response_object.title} edited successfully'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @role_required(['admin'])
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
    authentication_classes = [CustamizePermission]

    @role_required(['admin', 'organizer'])
    def get(self, request):
        registration_queryset = Registration.objects.all()
        serializer = ReportSerializer(registration_queryset, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class CountEventsAPI(APIView):
    authentication_classes = [CustamizePermission]

    @role_required(['admin', 'organizer'])
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
