from django.urls import path, include

urlpatterns = [
    path('pokemon/', include("pokemon.urls")),
]
