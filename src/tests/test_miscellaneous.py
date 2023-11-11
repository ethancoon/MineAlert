import unittest
from src.cogs.miscellaneous import Miscellaneous
from discord.ext import commands

class TestMiscellaneous(unittest.TestCase):
    def setUp(self) -> None:
        self.miscellaneous = Miscellaneous(commands.Bot)

    def test_generate_seed(self) -> None:
        seed = self.miscellaneous.helpers.generate_seed()

        self.assertTrue(isinstance(seed, str))
        self.assertTrue(0 < len(seed) <= 20)
        self.assertTrue(-9223372036854775808 <= int(seed) <= 9223372036854775807)


if __name__ == "__main__":
    unittest.main()