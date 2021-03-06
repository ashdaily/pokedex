import inspect
import os

from django.core.cache import cache
from django.test import TestCase


__all__ = [
    "TestCaseBaseClass", 
    "VALID_POKEMON_NAMES_LIST", 
    "INVALID_POKEMON_NAMES_LIST"
]


class TestCaseBaseClass(TestCase):
    def tearDown(self):
        """
        We don't want to use cache during unit tests.
        """
        cache.clear()

    def get_cassette(self, name=None):
        """
        Save the cassette in fixtures folder
        """
        stack = inspect.stack(0)[1]
        return os.path.join(os.path.dirname(stack[1]),
                            'fixtures/http_{cls}_{caller}{name}.yaml'.format(
                                cls=self.__class__.__name__,
                                caller=stack[3],
                                name='_' + name if name else ''))


VALID_POKEMON_NAMES_LIST = [
    "hatterene",
    "impidimp",
    "morgrem",
    "grimmsnarl",
    "obstagoon",
    "perrserker",
    "cursola",
    "sirfetchd",
    "mr-rime",
    "runerigus",
    "milcery",
    "alcremie",
    "falinks",
    "pincurchin",
    "snom",
    "frosmoth",
    "stonjourner",
    "morpeko",
    "cufant",
    "copperajah",
    "dracozolt",
    "arctozolt",
    "dracovish",
    "arctovish",
    "duraludon",
    "dreepy",
    "drakloak",
    "dragapult"
]

INVALID_POKEMON_NAMES_LIST = [
    "eiscue-ice",
    "indeedee-male",
    "deoxys-defense",
    "deoxys-speed",
    "wormadam-sandy",
    "wormadam-trash",
    "shaymin-sky",
    "giratina-origin",
    "rotom-heat",
    "rotom-wash",
    "rotom-frost",
    "rotom-fan",
    "rotom-mow",
    "castform-sunny",
    "castform-rainy",
    "castform-snowy",
    "basculin-blue-striped",
    "darmanitan-zen",
    "meloetta-pirouette",
    "tornadus-therian",
    "thundurus-therian",
    "landorus-therian",
    "kyurem-black",
    "kyurem-white",
    "keldeo-resolute",
    "meowstic-female",
    "aegislash-blade",
    "pumpkaboo-small",
    "pumpkaboo-large",
    "pumpkaboo-super",
    "gourgeist-small",
    "gourgeist-large",
    "gourgeist-super",
    "venusaur-mega",
    "charizard-mega-x",
    "charizard-mega-y",
    "blastoise-mega",
    "alakazam-mega",
    "gengar-mega",
    "kangaskhan-mega",
    "pinsir-mega",
    "gyarados-mega",
    "aerodactyl-mega",
    "mewtwo-mega-x",
    "mewtwo-mega-y",
    "ampharos-mega",
    "scizor-mega",
    "heracross-mega",
    "houndoom-mega",
    "tyranitar-mega",
    "blaziken-mega",
    "gardevoir-mega",
    "mawile-mega",
    "aggron-mega",
    "medicham-mega",
    "manectric-mega",
    "banette-mega",
    "absol-mega",
    "garchomp-mega",
    "lucario-mega",
    "abomasnow-mega",
    "floette-eternal",
    "latias-mega",
    "latios-mega",
    "swampert-mega",
    "sceptile-mega",
    "sableye-mega",
    "altaria-mega",
    "gallade-mega",
    "audino-mega",
    "sharpedo-mega",
    "slowbro-mega",
    "steelix-mega",
    "pidgeot-mega",
    "glalie-mega",
    "diancie-mega",
    "metagross-mega",
    "kyogre-primal",
    "groudon-primal",
    "rayquaza-mega",
    "pikachu-rock-star",
    "pikachu-belle",
    "pikachu-pop-star",
    "pikachu-phd",
    "pikachu-libre",
    "pikachu-cosplay",
    "hoopa-unbound",
    "camerupt-mega",
    "lopunny-mega",
    "salamence-mega",
    "beedrill-mega",
    "rattata-alola",
    "raticate-alola",
    "raticate-totem-alola",
    "pikachu-original-cap",
    "pikachu-hoenn-cap",
    "pikachu-sinnoh-cap",
    "pikachu-unova-cap",
    "pikachu-kalos-cap",
    "pikachu-alola-cap",
    "raichu-alola",
    "sandshrew-alola",
    "sandslash-alola",
]