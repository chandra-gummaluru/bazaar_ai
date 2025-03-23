from bazaar_ai import game, trader, market
from bazaar_ai.terms import GoodTypes, BonusTypes
import random

# Define the bonus for the Camel Good (bonus added to a trader's total coins)
CAMEL_BONUS = 5

# Define the available coin stacks for each type of good in the game
# Each good type has a list representing the quantity of coins available for each type in the stack.
COIN_STACKS = {
    GoodTypes.DIAMOND: [5, 5, 5, 7, 7],  # Diamond coin stacks
    GoodTypes.GOLD: [5, 5, 5, 6, 6],  # Gold coin stacks
    GoodTypes.SILVER: [5, 5, 5, 5, 5],  # Silver coin stacks
    GoodTypes.FABRIC: [1, 1, 2, 2, 3, 3, 5],  # Fabric coin stacks
    GoodTypes.SPICE: [1, 1, 2, 2, 3, 3, 5],  # Spice coin stacks
    GoodTypes.LEATHER: [1, 1, 1, 1, 1, 1, 2, 3, 4],  # Leather coin stacks
}

# Define the bonus coin stacks for different bonus types
# These stacks represent the available bonus coins a trader can earn based on different bonus types.
BONUS_COIN_STACKS = {
    BonusTypes.THREE: [3, 3, 2, 2, 2, 1, 1],  # Bonus type for 3 coins
    BonusTypes.FOUR: [6, 6, 5, 5, 4, 4],  # Bonus type for 4 coins
    BonusTypes.FIVE: [10, 10, 9, 8, 8],  # Bonus type for 5 coins
}

# Define the reserve quantities of each good available in the market
# This dictionary sets the initial stock of goods available in the market.
GOODS_RESERVE = {
    GoodTypes.DIAMOND: 6,  # Diamonds available
    GoodTypes.GOLD: 6,  # Gold available
    GoodTypes.SILVER: 6,  # Silver available
    GoodTypes.FABRIC: 8,  # Fabric available
    GoodTypes.SPICE: 8,  # Spice available
    GoodTypes.LEATHER: 10,  # Leather available
    GoodTypes.CAMEL: 11,  # Camels available (special good)
}

# Define the traders (players in the game)
# Here we create two traders with random actions. The Trader class should ideally
# be extended to include different types of strategies based on the select_action function.

# Trader 1: "Caveman" with a specific seed for random actions
trader1 = trader.Trader(
    name="Caveman",  # Name of the trader
    seed=321,  # Seed for random actions to ensure reproducibility
)

# Trader 2: "Villager" with a different seed for random actions
trader2 = trader.Trader(
    name="Villager",  # Name of the trader
    seed=247,  # Seed for random actions to ensure reproducibility
)

# List of traders participating in the game
traders = [trader1, trader2]

# Define the market instance
# The market manages the goods, coins, bonuses, and trader interactions during the game.
market = market.Market(
    seed=328,  # Seed for random market events
    coin_stacks=COIN_STACKS,  # Coin stacks per good type
    bonus_coin_stacks=BONUS_COIN_STACKS,  # Bonus coin stacks
    goods_reserve=GOODS_RESERVE,  # Initial goods reserve
    camel_bonus=CAMEL_BONUS,  # Camel bonus for traders
)

# Initialize the game with the traders and the market
# This sets up the game environment, preparing the market and traders for interaction.
g = game.Game(traders, market)
g.setup()

# Start the game and play for a specified number of rounds, with detailed verbosity
g.play(verbosity=game.Verbosity.ALL)

# After the game finishes, show the stats (final state of the game and traders)
g.show_stats()
