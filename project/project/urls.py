from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import environ
from rest_framework import permissions


env = environ.Env()
swagger_view = get_schema_view(
    openapi.Info(
        title=env("PROJECT_NAME"),
        default_version="v1",
        description="API to search pokemon names",
        terms_of_service="",
        contact=openapi.Contact(email="ashtokyo31@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    # Pokemon API
    path('pokemon/', include("pokemon.urls")),

    # Swagger
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        swagger_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        swagger_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
