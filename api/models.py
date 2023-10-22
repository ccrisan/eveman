from django.conf import settings
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024, blank=True)
    moment = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_events")
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="attended_events")
    max_attendees = models.SmallIntegerField(default=0)
