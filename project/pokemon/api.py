from django.conf import settings
import requests
from rest_framework.views import APIView, Response


POKEMON_API_URL = settings.POKEMON_API_URL
TRANSLATION_API_URL = settings.TRANSLATION_API_URL


class PokemonAPI(APIView):
    """
    PATH: /pokemon/<name>
    """
    lookup_field = "pokemon_name"

    def _get_description(self, flavor_text_entries):
        """
        filter english description
        clean the string by removing escape sequences
        """
        def _filter(x):
            if flavor["language"]["name"] == "en":
                return x["flavor_text"]
            return None
        en_descriptions = list(
            map(
                lambda x:x["flavor_text"] if x["language"]["name"] == "en" else None, 
                flavor_text_entries
            )
        )
        
        en_descriptions = [' '.join(d.split()) for d in en_descriptions if d is not None]
        en_descriptions = " ".join(en_descriptions)
        en_descriptions = en_descriptions.replace("\xad ", "").replace("\xad", "")
        return en_descriptions

    def get(self, request, *args, **kwargs):
        
        pokemon_name = kwargs.get("pokemon_name")
        
        r = requests.get(f"{POKEMON_API_URL}/{pokemon_name}")

        payload = {
            "name": r.json().get("name"),
            "is_legendary": r.json().get("is_legendary"),
            "habitat": r.json().get("habitat", {}).get("name"),
            "description": self._get_description(
                    r.json().get("flavor_text_entries")
                )
        }
        
        return Response(payload, status=r.status_code)