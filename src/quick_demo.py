from bazaar_ai import game, trader, market
from bazaar_ai.terms import GoodTypes, BonusTypes
import random

# Define the traders (players in the game)
# Here we create two traders with random actions. The Trader class should ideally
# be extended to include different types of strategies based on the select_action function.

trader1 = trader.Trader(
    name="Caveman",
    seed=321,
)
trader2 = trader.Trader(
    name="Villager",
    seed=247,
)

traders = [trader1, trader2]

# play a classic game
g = game.ClassicGame(traders)
g.setup()
g.play(verbosity=game.Verbosity.ALL)

g.show_stats()
