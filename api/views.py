from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .exceptions import PastEvent, TooManyAttendees
from .models import Event
from .serializers import RegisterSerializer, CreateEventSerializer, UpdateEventSerializer, ViewEventSerializer


class RegisterUserView(generics.CreateAPIView):
    """
    Register a new user.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ListCreateEventsView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        """
        List all existing events in the system.

        Request must include auth token.
        """

        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Add a new event to the system.

        Request must include auth token.
        """

        return super().post(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_class(self) -> type[Serializer]:
        if self.request.method == "POST":
            return CreateEventSerializer
        else:
            return ViewEventSerializer


class ListMyEventsView(generics.ListAPIView):
    """
    List all events that the current user has created.

    Request must include auth token.
    """

    serializer_class = ViewEventSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> models.QuerySet:
        # Restrict the list of events to only those created by current user
        return self.request.user.created_events.all()


class RetrieveUpdateEventView(generics.RetrieveUpdateAPIView):
    """
    Update an existing event.

    Request must include auth token. Only events created by current user can be updated.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        """
        Retrieve details about an event.

        Request must include auth token.
        """

        return super().get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        Update an existing event.

        Request must include auth token. Only events created by current user can be updated.
        """

        return super().patch(*args, **kwargs)

    def get_queryset(self) -> models.QuerySet:
        # Restrict the list of events to only those created by current user
        if self.request.method != "GET":
            return self.request.user.created_events.all()
        else:
            return Event.objects.all()

    def get_serializer_class(self) -> type[Serializer]:
        if self.request.method == "GET":
            return ViewEventSerializer
        else:
            return UpdateEventSerializer


class EventAttendanceView(generics.GenericAPIView):
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        """
        Register attendance of the current user to an event.

        Request must include auth token.
        """

        event = self.get_object()
        if 0 < event.max_attendees <= event.attendees.count():
            raise TooManyAttendees()
        if event.moment < datetime.utcnow():
            raise PastEvent()

        event.attendees.add(request.user)
        return Response(status=200)

    def delete(self, request, *args, **kwargs):
        """
        Unregister attendance of the current user to an event.

        Request must include auth token.
        """

        event = self.get_object()
        if event.moment < datetime.utcnow():
            raise PastEvent()

        event.attendees.remove(request.user)
        return Response(status=200)
