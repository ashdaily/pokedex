from unittest.mock import patch

import vcr
from django.urls import reverse

from .utils import (
    TestCaseBaseClass,
    VALID_POKEMON_NAMES_LIST, 
    INVALID_POKEMON_NAMES_LIST
)
from pokemon.api import BasePokemonAPI


class TestPokemonAPI(TestCaseBaseClass):
    record_mode = "none"

    def test_get_pokemon_information_by_name(self):
        with vcr.use_cassette(self.get_cassette(), record_mode=self.record_mode):
            url = reverse("pokemon-api", kwargs={"pokemon_name":"mewtwo"})
            r = self.client.get(url)

            self.assertEqual(
                set(r.json().keys()), 
                {"name", "is_legendary", "habitat", "description"}
            )
            self.assertEqual(r.status_code, 200)

    def test_get_pokemon_information_by_name_with_many_pokemon_names(self):
        with vcr.use_cassette(self.get_cassette(), record_mode=self.record_mode):
            # test valid pokemon names
            for pokemon_name in VALID_POKEMON_NAMES_LIST:
                url = reverse("pokemon-api", kwargs={"pokemon_name":pokemon_name})
                r = self.client.get(url)

                self.assertEqual(
                    set(r.json().keys()), 
                    {"name", "is_legendary", "habitat", "description"}
                )
                self.assertEqual(r.status_code, 200)

            # test if api can handle invalid pokemon names
            for pokemon_name in INVALID_POKEMON_NAMES_LIST:
                url = reverse("pokemon-api", kwargs={"pokemon_name":pokemon_name})
                r = self.client.get(url)
                self.assertEqual(r.status_code, 404)


class TestPokemonTranslatedAPI(TestCaseBaseClass):
    record_mode = "none"

    def test_get_pokemon_information_by_name_with_translation(self):
        with vcr.use_cassette(self.get_cassette(), record_mode=self.record_mode):        
            url = reverse(
                "pokemon-translated-api", 
                kwargs={"pokemon_name":"pikachu"}
            )
            r = self.client.get(url, kwargs={"pokemon_name":"pikachu"})
            self.assertEqual(
                set(r.json().keys()), 
                {"name", "is_legendary", "habitat", "description"}
            )
            self.assertEqual(r.status_code, 200)

    def test_get_translated_pokemon_does_yoda_translations_correctly(self):
        # when pokemon is legendary, test if api does yoda translations
        patch_payload = {
            "name": "mewtwo",
            "is_legendary": True,
            "habitat": "not_cave",
            "description": "It was created by a scientist after years of experiments."
        }
        with patch.object(
            BasePokemonAPI, '_make_response', return_value=patch_payload
        ):
            with vcr.use_cassette(self.get_cassette(), record_mode=self.record_mode):        
                url = reverse(
                    "pokemon-translated-api", 
                    kwargs={"pokemon_name":"mewtwo"}
                )
                r = self.client.get(url)
                
                self.assertEqual(
                    set(r.json().keys()), 
                    {"name", "is_legendary", "habitat", "description"}
                )
                self.assertEqual(r.status_code, 200)
                self.assertEqual(
                    r.json()["description"], 
                    "Created by a scientist after years of experiments,  it was."
                )

        # when pokemon is not legendary but habitat is cave, test if api does yoda translations
        patch_payload["is_legendary"] = False
        patch_payload["habitat"] = "cave"

        with patch.object(
            BasePokemonAPI, '_make_response', return_value=patch_payload
        ):
            with vcr.use_cassette(self.get_cassette(), record_mode=self.record_mode):        
                url = reverse(
                    "pokemon-translated-api", 
                    kwargs={"pokemon_name":"mewtwo"}
                )
                r = self.client.get(url)
                
                self.assertEqual(
                    set(r.json().keys()), 
                    {"name", "is_legendary", "habitat", "description"}
                )
                self.assertEqual(r.status_code, 200)
                self.assertEqual(
                    r.json()["description"], 
                    "Created by a scientist after years of experiments,  it was."
                )

    def test_get_translated_pokemon_does_shakespeare_translations_correctly(self):
        # when pokemon is not legendary and habitat is not cave
        patch_payload = {
            "name": "mewtwo",
            "is_legendary": False,
            "habitat": "not_cave",
            "description": "It was created by a scientist after years of experiments."
        }
        with patch.object(
            BasePokemonAPI, '_make_response', return_value=patch_payload
        ):
            with vcr.use_cassette(self.get_cassette(), record_mode=self.record_mode):        
                url = reverse(
                    "pokemon-translated-api", 
                    kwargs={"pokemon_name":"mewtwo"}
                )
                r = self.client.get(url)
                
                self.assertEqual(
                    set(r.json().keys()), 
                    {"name", "is_legendary", "habitat", "description"}
                )
                self.assertEqual(r.status_code, 200)
                self.assertEqual(
                    r.json()["description"], 
                    "'t wast did create by a scientist after years of experiments."
                )
        