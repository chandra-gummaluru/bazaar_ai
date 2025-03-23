from abc import ABC, abstractmethod
from .terms import GoodTypes, BonusTypes, Stats
from .actions import Take, Trade, Sell, Herd

import random

# formatting
bold = "\033[1m"
reset = "\033[0m"
fg_white = "\033[38;2;255;255;255m"
bg_black = "\033[48;2;0;0;0m"


class Trader:
    """
    Represents a trader participating in the market, holding goods and coins.

    Attributes:
        rng (random.Random): The random number generator used by the trader.
        name (str): The trader's name.
        hand (Hand): The goods currently in the trader's hand.
        satchel (Satchel): The trader's satchel for holding coins and bonus coins.
    """

    def __init__(self, seed, name):
        """
        Initializes a new trader with the given seed and name.

        Args:
            seed (int): The seed for random number generation.
            name (str): The name of the trader.
        """

        # use this for any random operations
        self._rng = random.Random(seed)

        self._name = name
        self._hand = Hand([])
        self._satchel = Satchel()

    @property
    def rng(self):
        return self._rng

    @property
    def name(self):
        return self._name

    @property
    def hand(self):
        return self._hand

    @property
    def satchel(self):
        return self._satchel

    def get_all_actions(self, market_observation):
        """
        Returns a list of all possible actions the trader can take based on the market observation.

        Args:
            market_observation (MarketObservation): The current state of the market.

        Returns:
            list: A list of possible actions.
        """

        actions = []
        actions += Take.get_all_actions(self.hand, market_observation)
        actions += Trade.get_all_actions(self.hand, market_observation)
        actions += Sell.get_all_actions(self.hand, market_observation)
        actions += Herd.get_all_actions(self.hand, market_observation)

        return actions

    @abstractmethod
    def select_action(self, market_observation):
        """
        Abstract method for selecting an action based on the market observation,
        the trader's hand, and his/her satchel.

        Args:
            market_observation (MarketObservation): The current state of the market.

        Returns:
            Action: The selected action.
        """
        actions = self.get_all_actions(market_observation)

        return self.rng.choice(actions)
        
    def summary(self):
        """
        Returns a string representation of the trader, including their hand and satchel.

        Returns:
            str: The string representation of the trader.
        """
        bold = "\033[1m"
        reset = "\033[0m"
        fg_white = "\033[38;2;255;255;255m"
        bg_black = "\033[48;2;0;0;0m"

        s = f"{bg_black}{fg_white}{self.name}{reset}\n"
        s += f"{bold}Hand:{reset}\n{self.hand.goods}\n{self.satchel}"

        return s

    def __str__(self):
        return self.summary()

        
class Hand:
    """
    Represents a hand used by a trader to hold goods.
    
    Attributes:
        goods (list): The list of goods in the hand.
    """
    
    def __init__(self, goods):
        self._goods = sorted(goods, key=lambda good: good.good_type.name)
        
    @property
    def goods(self):
        return self._goods
        
    def append(self, good):
        self.goods.append(good)
        self.goods.sort(key=lambda good: good.good_type.name)
    
    def remove(self, good):
        self.goods.remove(good)
        self.goods.sort(key=lambda good: good.good_type.name)
        
    def count_goods(self, include_all=False):
        count = 0
        for good in self.goods:
            if include_all or (good.good_type != GoodTypes.CAMEL):
                count += 1
        return count
                
    
    def __repr__(self):
        s = f""
        s += str(self.goods_reserve_count)
        
        goods_map = {}
        for good in self.goods:
            goods_map[good.good_type] = goods_map.get(good.good_type, 0) + 1
        
        for good_type in GoodTypes:
            if good_type != GoodTypes.CAMEL:
                s += "_" + str(good_type.name) + ":" + str(goods_map.get(good_type, 0)) + ":" + str(self.coin_stacks[good_type])
            
        return s
        
    def __eq__(self, other):
        # two hands are the same if they contain the same goods
        if isinstance(other, Hand):
            return repr(self) == repr(other)

    def __hash__(self):
        return hash(repr(self))
        
class Satchel:
    """
    Represents a satchel used by a trader to hold coins and bonus coins.

    Attributes:
        coins (list): The list of coins in the satchel.
        bonus_coins (dict): A dictionary of bonus coins categorized by bonus type.
    """

    def __init__(self):
        """
        Initializes a new satchel.
        """
        self._coins = []
        self._bonus_coins = {
            BonusTypes.THREE: [],
            BonusTypes.FOUR: [],
            BonusTypes.FIVE: [],
        }

    @property
    def coins(self):
        return self._coins

    def get_bonus_coin_count(self, bonus_type):
        """
        Returns the count of bonus coins of a specific type in the satchel.

        Args:
            bonus_type (BonusTypes): The type of bonus coin to count.

        Returns:
            int: The count of the specified bonus coins.
        """
        return len(self._bonus_coins[bonus_type])

    def add_coin(self, coin):
        """
        Adds a coin to the satchel.

        Args:
            coin (Coin): The coin to add.
        """
        self._coins.append(coin)

    def add_bonus_coin(self, bonus_coin):
        """
        Adds a bonus coin to the satchel.

        Args:
            bonus_coin (BonusCoin): The bonus coin to add.
        """
        self._bonus_coins[bonus_coin.bonus_type].append(bonus_coin)

    def calculate_points(self, include_bonus_coins=False):
        """
        Calculates the total points based on the coins and bonus coins in the satchel.

        Args:
            include_bonus_coins (bool): Whether to include bonus coins in the calculation.

        Returns:
            int: The total points.
        """
        points = 0
        for coin in self._coins:
            points += coin.value
        if include_bonus_coins:
            for bonus_coins_by_type in self._bonus_coins.values():
                for bonus_coin in bonus_coins_by_type:
                    points += bonus_coin.value
        return points
        
        
    def summary(self):
        """
        Returns a string representation of the satchel, including coins and bonus coins.

        Returns:
            str: The string representation of the satchel.
        """
        s = f"{bold}Satchel:{reset}\n{Stats.MONEY.value}: {self.calculate_points()} | "
        s += f"{BonusTypes.THREE.value}: {self.get_bonus_coin_count(BonusTypes.THREE)} "
        s += f"{BonusTypes.FOUR.value}: {self.get_bonus_coin_count(BonusTypes.FOUR)} "
        s += f"{BonusTypes.FIVE.value}: {self.get_bonus_coin_count(BonusTypes.FIVE)}"
        
        return s
    
    def __repr__(self):
        s = f""
        s += self.calculate_points()
        
        for bonus_type in BonusTypes:
            s += "_" + str(bonus_type.name) + ":" + str(self.get_bonus_coin_count(bonus_type))
            
        return s

    def __str__(self):
        return self.summary()
        
    def __eq__(self, other):
        # two satchels are the same if they contain the same number of points,
        # and bonus coins of each type
        if isinstance(other, Satchel):
            return repr(self) == repr(other)

    def __hash__(self):
        return hash(repr(s))
