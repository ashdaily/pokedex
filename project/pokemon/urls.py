from django.urls import path

from pokemon.api import PokemonAPI, PokemonTranslatedAPI


urlpatterns = [
    path(
        "<str:pokemon_name>",
        PokemonAPI.as_view(),
        name="pokemon-api"
    ),
    path(
        "translated/<str:pokemon_name>", 
        PokemonTranslatedAPI.as_view(), 
        name="pokemon-translated-api"
    )
]