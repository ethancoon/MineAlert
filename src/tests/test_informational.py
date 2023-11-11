import unittest
from src.cogs.informational import Informational
from discord.ext import commands

class TestInformational(unittest.TestCase):
    def setUp(self) -> None:
        self.informational = Informational(commands.Bot)
    
    def test_get_profile(self) -> None:
        username, uuid, skin_variant, uuid_exists = self.informational.helpers.get_profile("w1f1")
        
        self.assertTrue(isinstance(username, str))
        self.assertTrue(isinstance(uuid, str))
        self.assertTrue(isinstance(skin_variant, str))
        self.assertTrue(isinstance(uuid_exists, bool))
        self.assertTrue(len(username) > 0)
        self.assertTrue(len(uuid) > 0)
        self.assertTrue(len(skin_variant) > 0)
        self.assertTrue(uuid_exists)

    def test_get_player_images(self) -> None:
        full_body_url, thumbnail_url = self.informational.helpers.get_player_images("b1f1b9a4-4d8a-4d9b-9c0d-3d3a0b9a1b5a")

        self.assertTrue(isinstance(full_body_url, str))
        self.assertTrue(isinstance(thumbnail_url, str))
        self.assertTrue(len(full_body_url) > 0)
        self.assertTrue(len(thumbnail_url) > 0)


if __name__ == "__main__":
    unittest.main()