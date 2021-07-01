from rest_framework import generics

from pokemon.serializers import PokemonSerializer
from pokemon.models import Pokemon


class PokemonAPI(
    generics.RetrieveAPIView
):
    """
    PATH: /pokemon/<pokemon_name>
    """
    serializer_class = PokemonSerializer
    # queryset = Pokemon.objects.all()