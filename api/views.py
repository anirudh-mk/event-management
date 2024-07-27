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
    """
     API view to Event CRUD operation
     """
    # authendication to access token
    authentication_classes = [CustamizePermission]

    # role decorator for api access perimission
    @role_required(['admin', 'organizer'])
    def get(self, request, id=None):
        # check id present or not if id present return curresponding single instance
        if id:

            # if id pressent access event model with id
            event_queryset = Event.objects.filter(id=id).first()

            # if queryset not present return error response
            if not event_queryset:
                return Response(
                    data={"error": "invalid event id"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # if queyset is not none pass to serializer
            serializer = EventSerializer(event_queryset, many=False)

            # return serializer response
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        # if id not present fetch all event objects
        event_queryset = Event.objects.all()

        # pass queryset to serializer
        serializer = EventSerializer(event_queryset, many=True)

        # return serializer data
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    # post method for create event
    # role decorator for api access perimission
    @role_required(['admin'])
    def post(self, request):
        # pass data to serializer
        serializer = EventSerializer(data=request.data)

        # check serializer is valid
        if serializer.is_valid():
            response_object = serializer.save()

            # if serializer is valid creat event and pass instance to signal to notify user
            notification_signal.send(sender=response_object.__class__, instance=response_object)

            # return success response
            return Response(
                data={"response": f'{response_object.title} Created Successfully'},
                status=status.HTTP_200_OK
            )
        # if serializer is not valid error response
        return Response(data=serializer.errors)

    # patch method for create event
    # role decorator for api access perimission
    @role_required(['admin'])
    def patch(self, request, id):
        # fetch event queryset with id
        event_queryset = Event.objects.filter(id=id).first()

        # if queryset not found return error response
        if not event_queryset:
            return Response(
                data={"error": 'event not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        # pass queryset to serializer
        serializer = EventSerializer(event_queryset, data=request.data, partial=True)

        # check serializer is valid
        if serializer.is_valid():
            response_object = serializer.save()

            # if serializer is valid creat event and pass instance to signal to notify user
            update_notification_signal.send(sender=response_object.__class__, instance=response_object)

            # return success response
            return Response(
                data={"success": f'{response_object.title} edited successfully'},
                status=status.HTTP_200_OK
            )
        # if serializer is not valid send serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete method for delete event
    # role decorator for api access perimission
    @role_required(['admin'])
    def delete(self, request, id):

        # fetch event queryset with id
        event_queryset = Event.objects.filter(id=id).first()

        # if queryset not peresent return error response
        if not event_queryset:
            return Response(
                data={"error": "event not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        # if queryset present return success response and deleter queryset
        event_queryset.delete()
        return Response(
            data={"success": "Event deleted successfully"},
            status=status.HTTP_200_OK
        )


class EventRegisterAPI(APIView):
    """
     API View to event registration
     """
    def post(self, request):
        # pass data to serializer for validation
        serializer = EventRegisterSerializer(data=request.data)

        # check serializer is valid
        if serializer.is_valid():
            response_object = serializer.save()

            # if serializer is valid return success response
            return Response(
                data={"success": f"registration to {response_object.event.title} successfull"},
                status=status.HTTP_200_OK
            )

        # else return serializer errors/
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ReportAPI(APIView):
    """
     API view to Registration report.
     """
    # authendication to access token
    authentication_classes = [CustamizePermission]

    # role decorator for api access perimission
    @role_required(['admin', 'organizer'])
    def get(self, request):
        # access all registration objects

        registration_queryset = Registration.objects.all()
        # pass registration queryset to serializer for validation

        serializer = ReportSerializer(registration_queryset, many=True)

        # return serializer data on response
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class CountEventsAPI(APIView):
    """
     API view to Count event.
     """

    # authendication to access token
    authentication_classes = [CustamizePermission]

    # role decorator for api access perimission
    @role_required(['admin', 'organizer'])
    def get(self, request):

        # count all objects in registration
        registration_count = Registration.objects.count()

        # count all objects in event
        event_count = Event.objects.count()

        # return registration count and event count in response
        return Response(
            data={
                "registration_count": registration_count,
                "event_count": event_count
            },
            status=status.HTTP_200_OK
        )
