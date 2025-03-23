import random
from .pieces.coins import Coin, BonusCoin
from .pieces.goods import Good
from .terms import GoodTypes, ActionTypes, BonusTypes, Stats

from copy import deepcopy

# formatting
bold = "\033[1m"
reset = "\033[0m"
fg_white = "\033[38;2;255;255;255m"
bg_black = "\033[48;2;0;0;0m"


class Market:
    """
    Represents a market where goods, coins, and bonus coins are available for trading.

    Attributes:
        camel_bonus (int): The bonus for having camels in a trade.
        hand_limit (int): The hand limit for the traders.
        rng (random.Random): The random number generator for the market.
        coin_stacks (dict): The available stacks of coins for each good type.
        bonus_coin_stacks (dict): The available stacks of bonus coins for each bonus type.
        goods_reserve (list): The reserve of goods available for sale.
        goods (list): The goods currently available for sale in the market.
        goods_sold (list): The list of goods that have been sold.
    """

    def __init__(
        self, seed, coin_stacks, bonus_coin_stacks, goods_reserve, camel_bonus, hand_limit
    ):
        """
        Initializes the market with a given seed, stacks of coins, bonus coins, goods reserve, and camel bonus.

        Args:
            seed (int): The seed for random number generation.
            coin_stacks (dict): The initial coin stacks for each good type.
            bonus_coin_stacks (dict): The initial bonus coin stacks for each bonus type.
            goods_reserve (dict): The initial reserve of goods available in the market.
            camel_bonus (int): The bonus applied for having camels in the market.
            hand_limit (int): The hand limit for the traders.
        """

        # use this for random operations
        self._rng = random.Random(seed)

        self._camel_bonus = camel_bonus

        self._coin_stacks = {}
        self._bonus_coin_stacks = {}
        self._goods_reserve = []
        self._goods = []
        self._goods_sold = []

        self._setup_coins(coin_stacks)
        self._setup_bonus_coins(bonus_coin_stacks)
        self._setup_goods(goods_reserve)
        self._refill_market()
        
        self._hand_limit = hand_limit
    
    @property
    def hand_limit(self):
        return self._hand_limit
        
    @property
    def camel_bonus(self):
        return self._camel_bonus

    @property
    def rng(self):
        return self._rng

    @property
    def coin_stacks(self):
        return self._coin_stacks

    @property
    def bonus_coin_stacks(self):
        return self._bonus_coin_stacks

    @property
    def goods_reserve(self):
        return self._goods_reserve

    @property
    def goods(self):
        return self._goods

    @property
    def goods_sold(self):
        return self._goods_sold

    def _setup_coins(self, coin_stacks):
        for good_type, values in coin_stacks.items():
            self.coin_stacks[good_type] = [Coin(good_type, value) for value in values]

    def _setup_bonus_coins(self, bonus_coin_stacks):
        for bonus_type, values in bonus_coin_stacks.items():
            self.bonus_coin_stacks[bonus_type] = [
                BonusCoin(bonus_type, value) for value in values
            ]
            random.shuffle(self.bonus_coin_stacks[bonus_type])

    def _setup_goods(self, goods_reserve):
        for good_type, count in goods_reserve.items():
            for _ in range(count):
                self.goods_reserve.append(Good(good_type))
        self.rng.shuffle(self.goods_reserve)

    def _refill_market(self):
        while len(self.goods) < 5:
            if self.goods_reserve:
                self.goods.append(self.goods_reserve.pop())
            else:
                break

    def observe_market(self):
        """
        Returns an observation of the current state of the market.

        Returns:
            MarketObservation: The market's current goods, coin stacks, and bonus coin counts.
        """

        # these lists can be modified without affecting the originals
        goods_copy = [good for good in self.goods]
        coin_stacks_copy = deepcopy(self.coin_stacks)
        bonus_coin_stacks_counts = {
            bonus_type: len(self.bonus_coin_stacks[bonus_type])
            for bonus_type in self.bonus_coin_stacks.keys()
        }
        market_observation = MarketObservation(
            goods_copy, len(self.goods_reserve), coin_stacks_copy, bonus_coin_stacks_counts,
            self.hand_limit
        )
        return market_observation

    def remove_coins(self, good_type, count):
        """
        Removes a specific number of coins of a given type from the market.

        Args:
            good_type (GoodTypes): The type of good to remove coins for.
            count (int): The number of coins to remove.

        Returns:
            list: The list of removed coins.
        """
        removed_coins = []
        for i in range(count):
            if len(self.coin_stacks[good_type]) > 0:
                removed_coins.append(self.coin_stacks[good_type].pop())
        return removed_coins

    def apply_action(self, trader, action):
        """
        Applies an action (such as take, sell, trade, or herd) to the market and trader.

        Args:
            trader (Trader): The trader applying the action.
            action (Action): The action to apply.

        Returns:
            None
        """
        if action.type == ActionTypes.TAKE:
            trader.hand.append(action.requested)
            self.goods.remove(action.requested)
            self._refill_market()

        if action.type == ActionTypes.SELL:
            for good in action.offered:
                trader.hand.remove(good)
                self.goods_sold.append(good)
            for good in action.offered:
                if not self.coin_stacks[good.good_type]:
                    break
                coin = self.coin_stacks[good.good_type].pop()
                trader.satchel.add_coin(coin)
            if len(action.offered) == 3 and self.bonus_coin_stacks[BonusTypes.THREE]:
                coin = self.bonus_coin_stacks[BonusTypes.THREE].pop()
                trader.satchel.add_bonus_coin(coin)
            if len(action.offered) == 4 and self.bonus_coin_stacks[BonusTypes.FOUR]:
                coin = self.bonus_coin_stacks[BonusTypes.FOUR].pop()
                trader.satchel.add_bonus_coin(coin)
            if len(action.offered) == 5 and self.bonus_coin_stacks[BonusTypes.FIVE]:
                coin = self.bonus_coin_stacks[BonusTypes.FIVE].pop()
                trader.satchel.add_bonus_coin(coin)
            self._refill_market()

        if action.type == ActionTypes.TRADE:
            for good in action.offered:
                trader.hand.remove(good)
                self.goods.append(good)
            for good in action.requested:
                trader.hand.append(good)
                self.goods.remove(good)

        if action.type == ActionTypes.HERD:
            for good in action.requested:
                self.goods.remove(good)
                trader.hand.append(good)
            self._refill_market()

    def is_market_closed(self):
        """
        Determines if the market is closed based on certain conditions.

        Returns:
            bool: True if the market is closed, otherwise False.
        """
        if len(self.goods) < 5 and len(self.goods_reserve) == 0:
            return True
        coin_stacks_exhausted_count = sum(
            len(stack) == 0 for stack in self.coin_stacks.values()
        )
        if coin_stacks_exhausted_count >= 3:
            return True
        return False

    def summary(self, full = True):
        """
        Returns a summary of the market's current state.

        Returns:
            str: The summary string.
            full (bool): Whether to return the full summary or not.
        """
        if full:
            s = f"{bg_black}{fg_white}{bold}Market{reset}\n"
            s += f"{bold}Goods Reserve:{reset} " + str(len(self.goods_reserve)) + "\n"
            s += f"{bold}Goods:{reset}\n" + str(self.goods) + f"\n{bold}Coins:{reset}\n"
            for good_type in self.coin_stacks.keys():
                s += f"{good_type.value}: {self.coin_stacks[good_type]}\n"
            s += f"{bold}Bonus Coins:{reset}\n"
            for bonus_type in self.bonus_coin_stacks.keys():
                s += f"{bonus_type.value}: {len(self.bonus_coin_stacks[bonus_type])} "
            return s
        else:
            s = f"{bg_black}{fg_white}{bold}Market:{reset}\n"
            s += f"{bold}GoodTypes Left:{reset} " + str(len(self.goods_reserve)) + "\n"
            s += f"{bold}GoodTypes:{reset}\n" + str(self.goods) + f"\n{bold}Coins:{reset}"
        return s
           
    def __str__(self):
        return self.summary(full = True)


class MarketObservation:
    """
    Represents an observation of the market state, including goods and coin stacks.

    Attributes:
        goods (list): The list of goods currently available in the market.
        goods_reserve_count (int): The number of goods left in the reserve.
        coin_stacks (dict): The available coin stacks for each good type.
        bonus_coin_stacks_counts (dict): The count of available bonus coins for each bonus type.
        hand_limit (int): The hand limit for the traders.
    """

    def __init__(
        self, goods, goods_reserve_count, coin_stacks, bonus_coin_stacks_counts, hand_limit
    ):
        """
        Initializes a market observation.

        Args:
            goods (list): The list of goods in the market.
            goods_reserve_count (int): The number of goods left in the reserve.
            coin_stacks (dict): The current coin stacks for each good type.
            bonus_coin_stacks_counts (dict): The count of each bonus coin type.
            hand_limit (int): The hand limit for the traders.
        """
        self._goods = sorted(goods, key=lambda good: good.good_type.name)
        self._goods_reserve_count = goods_reserve_count
        self._coin_stacks = coin_stacks
        self._bonus_coin_stacks_counts = bonus_coin_stacks_counts
        self._hand_limit = hand_limit
    
    def summary(self):
        s = f""
        s += str(self.goods_reserve_count)
        
        goods_map = {}
        for good in self.goods:
            goods_map[good.good_type] = goods_map.get(good.good_type, 0) + 1
        
        for good_type in GoodTypes:
            if good_type != GoodTypes.CAMEL:
                s += "_" + str(good_type.name) + ":" + str(goods_map.get(good_type, 0)) + ":" + str(self.coin_stacks[good_type])
        
        for bonus_type in BonusTypes:
            s += "_" + str(bonus_type.name) + ":" + str(self.bonus_coin_stacks_counts[bonus_type])
            
        return s
        
    def __str__(self):
        return self.summary()
        
    def __eq__(self, other):
        # two market observations are the same if they have identical goods
        # and coin stacks, the same number of bonus coins of each type,
        # and the same number of goods in the goods reserve
        if isinstance(other, MarketObservation):
            return (self.goods == other.goods
                and self.coin_stacks == other.coin_stacks
                and self.bonus_coin_stacks_counts == other.bonus_coin_stacks_counts
                and self.hand_limit == other.hand_limit)
    
    def __hash__(self):
        return hash(str(self))

    @property
    def goods(self):
        return self._goods

    @property
    def goods_reserve_count(self):
        return self._goods_reserve_count

    @property
    def coin_stacks(self):
        return self._coin_stacks

    @property
    def bonus_coin_stacks_counts(self):
        return self._bonus_coin_stacks_counts
        
    @property
    def hand_limit(self):
        return self._hand_limit
