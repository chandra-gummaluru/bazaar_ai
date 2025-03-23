from enum import Enum
from .terms import GoodTypes, BonusTypes, Stats
from .market import Market

class Verbosity(Enum):
    """
    Enum for verbosity levels in displaying the game state.
    """
    NONE = 0
    SOME = 1
    ALL = 2
    

class Game:
    """
    Represents a game involving two traders and a market.

    Attributes:
        traders (list): A list of the traders involved in the game.
        market (Market): The market where goods are traded.
        current_trader_index (int): The index of the current trader in the game.
        round (int): The current round of the game.
    """
    
    def __init__(self, traders, market):
        """
        Initializes the game with the given traders and market.

        Args:
            traders (list): The list of traders involved in the game.
            market (Market): The market for trading goods.
        """
        
        self.traders = traders
        self.market = market
        self.current_trader_index = 0
        self.round = 1
        
    def setup(self):
        """
        Sets up the initial game state by giving each trader some goods.

        Returns:
            None
        """
        
        for _ in range(5):
            good = self.market.goods_reserve.pop()
            self.traders[0].hand.append(good)
            good = self.market.goods_reserve.pop()
            self.traders[1].hand.append(good)
        self.show_state(verbosity = Verbosity.ALL)


    def show_state(self, verbosity = Verbosity.ALL):
        """
        Displays the current state of the game, including the market and traders' status.

        Args:
            verbosity (Verbosity): The level of verbosity for the display.

        Returns:
            None
        """
            
        if verbosity == Verbosity.NONE:
            return
        
        print("\n" + "="*50)
        print(f"Round {self.round}")
        print(f"{self.traders[self.current_trader_index].name}'s Turn")
        if verbosity.value >= Verbosity.SOME.value:
          print(self.market)
          print(self.traders[0])
          print(self.traders[1])
        else:
          print(self.market.summary())
        print("="*50)

    def show_stats(self):
        """
        Displays the scores of both traders, including bonus points for camels.

        Returns:
            None
        """
        
        # compute each trader's score
        trader1_score = self.traders[0].satchel.calculate_points(include_bonus_coins = True)
        trader2_score = self.traders[1].satchel.calculate_points(include_bonus_coins = True)

        # determine which trader has more camels
        trader1_camel_count = sum(1 for good in self.traders[0].hand.goods if good.good_type == GoodTypes.CAMEL)
        trader2_camel_count = sum(1 for good in self.traders[1].hand.goods if good.good_type == GoodTypes.CAMEL)

        if trader1_camel_count > trader2_camel_count:
            trader1_score += self.market.camel_bonus
        elif trader2_camel_count > trader1_camel_count:
            trader2_score += self.market.camel_bonus

        bold = "\033[1m"
        reset = "\033[0m"
        fg_white = "\033[38;2;255;255;255m"
        bg_black = "\033[48;2;0;0;0m"

        print(f"="*50)
        print("Results:")
        print(f"{bg_black}{fg_white}{self.traders[0].name}{reset}\n{Stats.MONEY.value}: {trader1_score}")
        print(f"{bg_black}{fg_white}{self.traders[1].name}{reset}\n{Stats.MONEY.value}: {trader2_score}")
        print(f"="*50)

    def play(self, verbosity = Verbosity.ALL, rounds = 1000):
        """
        Runs the game loop (up to the specified number of rounds), alternating turns between traders and managing market transactions.

        The function coordinates the market activities, allows traders to make decisions, and applies the results of their actions. It also updates the game state and displays the current status based on the verbosity level.

        Args:
            verbosity (Verbosity, optional): The level of verbosity for displaying the game state. 
                - Verbosity.NONE: No game state displayed.
                - Verbosity.SOME: Some details of the game state displayed.
                - Verbosity.ALL: Full game state displayed. Defaults to Verbosity.ALL.
            rounds (int): The maximum number of rounds to play in the game.

        Returns:
            None
        """
        print("="*50)
        print("Market Open")
        while not self.market.is_market_closed():
            current_trader = self.traders[self.current_trader_index]
            current_market_observation = self.market.observe_market()
            current_trader_action = current_trader.select_action(current_market_observation)
            
            if verbosity.value > Verbosity.NONE.value:
                print(current_trader.name + "'s Turn")
                print(current_trader_action)
            
            self.market.apply_action(current_trader, current_trader_action)
            self.current_trader_index = (self.current_trader_index + 1) % 2
            self.round += 1
            self.show_state(verbosity)
        print("Market Closed")
        
        
class ClassicGame(Game):
    def __init__(self, traders):
        # Define the bonus for the Camel Good (bonus added to a trader's total coins)
        CAMEL_BONUS = 5
        
        # Define the hand limit
        HAND_LIMIT = 7

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
        
        # Define the market instance
        # The market manages the goods, coins, bonuses, and trader interactions during the game.
        market = Market(
            seed=328,  # Seed for random market events
            coin_stacks=COIN_STACKS,  # Coin stacks per good type
            bonus_coin_stacks=BONUS_COIN_STACKS,  # Bonus coin stacks
            goods_reserve=GOODS_RESERVE,  # Initial goods reserve
            camel_bonus=CAMEL_BONUS,  # Camel bonus for traders
            hand_limit=HAND_LIMIT, # Hand limit for traders
        )
        
        super().__init__(traders, market)