from django.test import TestCase
from django.urls import reverse


class TestPokemonAPI(TestCase):

    def test_get_pokemon_information_by_name(self):
        url = reverse("pokemon-api", kwargs={"pokemon_name":"pikachu"})
        r = self.client.get(url)
        self.assertEqual(
            set(r.json().keys()), 
            {"name", "is_legendary", "habitat", "description"}
        )
        self.assertEqual(r.status_code, 200)

    def test_get_pokemon_information_by_name_with_translation(self):
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