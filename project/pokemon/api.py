from django.conf import settings
import requests
from rest_framework.views import APIView, Response


POKEMON_API_URL = settings.POKEMON_API_URL
TRANSLATION_API_URL = settings.TRANSLATION_API_URL


class BasePokemonAPI:
    def _make_response(self, response):
        habitat = response.json().get("habitat")
        habitat = habitat.get("name") if habitat else None

        payload = {
            "name": response.json().get("name"),
            "is_legendary": response.json().get("is_legendary"),
            "habitat": habitat,
            "description": self._get_description(
                    response.json().get("flavor_text_entries")
                )
        }
        return payload

    def _get_description(self, flavor_text_entries):
        """
        Filter english description
        Clean the string by removing escape sequences
        """
        if len(flavor_text_entries) == 0:
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


class PokemonAPI(APIView, BasePokemonAPI):
    """
    PATH: /pokemon/<name>
    """

    def get(self, request, *args, **kwargs):
        pokemon_name = kwargs.get("pokemon_name")
        
        r = requests.get(f"{POKEMON_API_URL}/{pokemon_name}")
        if r.ok:
            payload = self._make_response(r)
        else:
            payload = None
        
        return Response(payload, status=r.status_code)


class PokemonTranslatedAPI(APIView, BasePokemonAPI):
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

    def _extract_translation(self, response):
        translation = response.json().get("contents")
        if translation:
            return translation.get("translated")
        else:
            None

    def _make_response(self, r):
        payload = super()._make_response(r)

        if any([payload["habitat"] == "cave", payload["is_legendary"]]):
            # get yoda translation translated description
            r = self._get_translation(payload["description"], type="yoda")
            if r.ok:
                translation = self._extract_translation(r)
                if translation:
                    payload["description"] = translation
                    return payload

        # get shakespeare translated description
        r = self._get_translation(payload["description"])
        if r.ok:
            translation = self._extract_translation(r)
            if translation:
                payload["description"] = translation
                return payload

        # send normal description
        return payload

    def get(self, request, *args, **kwargs):
        pokemon_name = kwargs.get("pokemon_name")
        r = requests.get(f"{POKEMON_API_URL}/{pokemon_name}")
        if r.ok:
            payload = self._make_response(r)
        else:
            payload = None
        return Response(payload, status=r.status_code)