from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import RegisterUserView, ListCreateEventsView, ListMyEventsView, RetrieveUpdateEventView, EventAttendanceView


urlpatterns = [
    # User management
    path("register/", RegisterUserView.as_view(), name="register"),

    # Auth token management
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Event management
    path("events/", ListCreateEventsView.as_view(), name="events"),
    path("events/my/", ListMyEventsView.as_view(), name="my_events"),
    path("events/<int:pk>/", RetrieveUpdateEventView.as_view(), name="event"),
    path("events/<int:pk>/attendance/", EventAttendanceView.as_view(), name="event_attendance"),

    # API Schema/Swagger
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
