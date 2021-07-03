from django.urls import path

from pokemon.api import PokemonAPI


urlpatterns = [
    path(
        "<str:pokemon_name>",
        PokemonAPI.as_view(),
        name="pokemon-api"
    ),
    path(
        "<str:pokemon_name>", 
        PokemonAPI.as_view(), 
        name="pokemon-translated-api"
    )
]