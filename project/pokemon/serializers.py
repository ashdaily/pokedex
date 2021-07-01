from rest_framework.serializers import ModelSerializer

from pokemon.models import Pokemon


class PokemonSerializer(ModelSerializer):
    class Meta:
        model = Pokemon
        read_only_fields = [
            "name",
            "description",
            "habitat",
            "is_legendary"
        ]
