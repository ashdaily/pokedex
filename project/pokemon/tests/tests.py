from django.test import TestCase
from django.urls import reverse


class TestPokemonAPI(TestCase):

    def test_get_pokemon_by_name(self):
        url = reverse("pokemon-api", kwargs={"pokemon_name":"pikachu"})
        r = self.client.get(url)

        self.assertEqual(r.status_code, 200)