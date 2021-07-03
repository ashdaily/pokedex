from django.conf import settings
import requests
from rest_framework.views import APIView, Response


POKEMON_API_URL = settings.POKEMON_API_URL
TRANSLATION_API_URL = settings.TRANSLATION_API_URL


class BasePokemonAPI:
    def _get_description(self, flavor_text_entries):
        """
        Filter english description
        Clean the string by removing escape sequences
        """
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


class PokemonAPI(APIView, BasePokemonAPI):
    """
    PATH: /pokemon/<name>
    """

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


class PokemonTranslatedAPI(APIView):
    """
    PATH: /pokemon/translated/<name>
    """

    def _get_translation(self, text, type="shakespeare"):
        url = f"{TRANSLATION_API_URL}/{type}"
        r = requests.post(
            url,
            data={"text": text}
        )
        return r

    def _make_response(self, r):
        name = r.json().get("name")
        is_legendary = r.json().get("is_legendary")
        habitat = r.json().get("habitat", {}).get("name")
        description = self._get_description(
            r.json().get("flavor_text_entries")
        )

        payload = {
            "name": name,
            "is_legendary": is_legendary,
            "habitat": habitat,
            "description": description
        }

        if any(habitat == "cave", is_legendary):
            # get yoda translation
            r = self._get_translation(description, type="yoda")
            if r.ok:
                translation = r.json().get("contents", {}).get("translated")
                if translation:
                    payload["description"] = translation
                    return payload

        # get shakespeare translation
        r = self._get_translation(description)
        if r.ok:
            translation = r.json().get("contents", {}).get("translated")
            if translation:
                payload["description"] = translation
                return payload

        return payload

    def get(self, request, *args, **kwargs):
        pokemon_name = kwargs.get("pokemon_name")
        r = requests.get(f"{POKEMON_API_URL}/{pokemon_name}")
        payload = self._make_response(r)
        return Response(payload, status=r.status_code)