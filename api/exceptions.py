from rest_framework.exceptions import APIException


class TooManyAttendees(APIException):
    status_code = 400
    default_detail = 'The maximum number of attendees for this event has been already reached.'
    default_code = 'too_many_attendees'


class PastEvent(APIException):
    status_code = 400
    default_detail = 'The event is in the past.'
    default_code = 'past_event'
