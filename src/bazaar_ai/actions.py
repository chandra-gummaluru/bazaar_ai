from itertools import combinations
from collections import Counter
from .terms import GoodTypes, ActionTypes


class Action:
    """
    Abstract base class for all actions in the game.
    This class defines the interface for specific action types such as Herd, Sell, Take, and Trade.
    """

    pass


class Herd(Action):
    """
    Represents the action of herding camels from the market.

    Attributes:
        requested (list): A list of camels requested for herding.

    Methods:
        is_legal(): Determines if the herd action is legal.
        get_all_actions(hand, market_observation): Returns a list of all legal Herd actions based on the market.
    """

    def __init__(self, requested):
        """
        Initializes the Herd action with the requested camels.

        Args:
            requested (list): A list of camels to be herded.
        """
        self.type = ActionTypes.HERD
        self._requested = sorted(requested, key=lambda good: good.good_type.name)

    def _is_legal(self):
        """
        Checks if the herd action is legal.
        The action is legal if all requested goods are camels and at least one camel is requested.

        Returns:
            bool: True if the action is legal, otherwise False.
        """
        return (
            all(c.good_type == GoodTypes.CAMEL for c in self.requested)
            and len(self.requested) > 0 and len(self.requested)
        )
        
    @property
    def requested(self):
        """Returns the list of requested camels."""
        return self._requested

    @staticmethod
    def get_all_actions(hand, market_observation):
        """
        Returns all legal Herd actions based on the player's hand and market observation.

        Args:
            hand (list): The player's hand.
            market_observation (MarketObservation): The current state of the market.

        Returns:
            list: A list of legal Herd actions.
        """
        camels_in_market = [
            c for c in market_observation.goods if c.good_type == GoodTypes.CAMEL
        ]
        
        if camels_in_market:
            return [Herd(camels_in_market)]
        return []
        
    def summary(self):
        """Returns a string representation of the Herd action."""
        return f"Herd({len(self.requested)}x{GoodTypes.CAMEL.value})"
    
    def __repr__(self):
        return self.summary()
    
    def __str__(self):
        return self.summary()
        
    def __eq__(self, other):
        # two Herd actions are equal if they involve the same number of camels
        return len(self.requested) == len(other.requested)
     


class Sell(Action):
    """
    Represents the action of selling goods (excluding camels).

    Attributes:
        offered (list): A list of goods offered for sale.

    Methods:
        is_legal(): Determines if the sell action is legal.
        get_all_actions(hand, market_observation): Returns a list of all legal Sell actions based on the market.
    """

    def __init__(self, offered):
        """
        Initializes the Sell action with the offered goods.

        Args:
            offered (list): A list of goods offered for sale.
        """
        self.type = ActionTypes.SELL
        self._offered = sorted(offered, key=lambda good: good.good_type.name)

    @property
    def offered(self):
        """Returns the list of offered goods."""
        return self._offered

    def _is_legal(self):
        """
        Checks if the sell action is legal.
        The action is legal if the offered goods are not camels and meet specific conditions for diamond, gold, and silver.

        Returns:
            bool: True if the action is legal, otherwise False.
        """
        if not self.offered:
            return False
        good = self.offered[0].good_type
        if any(c.good_type != good for c in self.offered):
            return False
        if good == GoodTypes.CAMEL:
            return False
        if (
            good in (GoodTypes.DIAMOND, GoodTypes.GOLD, GoodTypes.SILVER)
            and len(self.offered) < 2
        ):
            return False
        return True

    def summary(self):
        """Returns a string representation of the Sell action."""
        return f"Sell({len(self.offered)}x{self.offered[0].good_type.value})"
        
    def __repr__(self):
        return self.summary()
        
    def __str__(self):
        return self.summary()
        
    def __eq__(self, other):
        # two Sell actions are equal the goods being offered are the same
        if isinstance(other, Sell):
            return self.offered == other.offered
            
    def __hash__(self):
        return hash(self.offered)

    @staticmethod
    def get_all_actions(hand, market_observation):
        """
        Returns all legal Sell actions based on the player's hand and market observation.

        Args:
            hand (list): The player's hand.
            market_observation (MarketObservation): The current state of the market.

        Returns:
            list: A list of legal Sell actions.
        """
        actions = []
        goods_by_type = {}
        for good in hand.goods:
            if good.good_type == GoodTypes.CAMEL:
                continue
            goods_by_type.setdefault(good.good_type, []).append(good)

        for all_goods in goods_by_type.values():
            for k in range(1, len(all_goods) + 1):
                candidate = all_goods[:k]
                action = Sell(candidate)
                if action._is_legal():
                    actions.append(action)
        return actions
        

class Take(Action):
    """
    Represents the action of taking a single good (excluding camels) from the market.

    Attributes:
        requested (Good): The requested good to be taken from the market.

    Methods:
        is_legal(): Determines if the take action is legal.
        get_all_actions(hand, market_observation): Returns a list of all legal Take actions based on the market.
    """

    def __init__(self, requested):
        """
        Initializes the Take action with the requested good.

        Args:
            requested (Good): A single good requested from the market.
        """
        self.type = ActionTypes.TAKE
        self.requested = requested
        
    def _is_legal(self):
        """
        Checks if the take action is legal.
        The action is legal if the requested good is not a camel.

        Returns:
            bool: True if the action is legal, otherwise False.
        """
        return self.requested.good_type != GoodTypes.CAMEL

    @staticmethod
    def get_all_actions(hand, market_observation):
        """
        Returns all legal Take actions based on the player's hand and market observation.

        Args:
            hand (list): The player's hand.
            market_observation (MarketObservation): The current state of the market.

        Returns:
            list: A list of legal Take actions.
        """
        actions = []
        for good in market_observation.goods:
            action = Take(good)
            if action._is_legal():
                if hand.count_goods() + 1 <= market_observation.hand_limit:
                    actions.append(action)
        return actions
    
    def summary(self):
        """Returns a string representation of the Take action."""
        return f"Take({self.requested.good_type.value})"
        
    def __repr__(self):
        return self.summary()
        
    def __str__(self):
        return self.summary()
        
    def __eq__(self, other):
        # two Take actions are equal the good being taken is the same
        if isinstance(other, Take):    
            return self.requested == other.requested
            
    def __hash__(self):
        return hash(self.requested)


class Trade(Action):
    """
    Represents the action of trading goods with the market.

    Attributes:
        offered (list): A list of goods offered for trade.
        requested (list): A list of goods requested in exchange.

    Methods:
        is_legal(): Determines if the trade action is legal.
        get_all_actions(hand, market_observation): Returns a list of all legal Trade actions based on the market.
    """

    def __init__(self, offered, requested):
        """
        Initializes the Trade action with the offered and requested goods.

        Args:
            offered (list): A list of goods offered for trade.
            requested (list): A list of goods requested in exchange.
        """
        self.type = ActionTypes.TRADE
        self._offered = sorted(offered, key=lambda good: good.good_type.name)
        self._requested = sorted(requested, key=lambda good: good.good_type.name)

    @property
    def offered(self):
        """Returns the list of offered goods."""
        return self._offered

    @property
    def requested(self):
        """Returns the list of requested goods."""
        return self._requested

    def _is_legal(self):
        """
        Checks if the trade action is legal.
        The action is legal if the offered and requested goods are valid, not including camels, and there are no overlapping goods between offered and requested.

        Returns:
            bool: True if the action is legal, otherwise False.
        """
        if not self.offered or not self.requested:
            return False
        if len(self.offered) != len(self.requested):
            return False
        if any(c.good_type == GoodTypes.CAMEL for c in self.requested):
            return False
        offered_types = {card.good_type for card in self.offered}
        requested_types = {card.good_type for card in self.requested}
        if not offered_types.isdisjoint(requested_types):
            return False
        return True

    @staticmethod
    def get_all_actions(hand, market_observation):
        """
        Returns all legal Trade actions based on the player's hand and market observation.

        Args:
            hand (list): The player's hand.
            market_observation (MarketObservation): The current state of the market.

        Returns:
            list: A list of legal Trade actions.
        """
        actions = []
        hand_goods = [c for c in hand.goods if c.good_type != GoodTypes.CAMEL]
        camels = [c for c in hand.goods if c.good_type == GoodTypes.CAMEL]
        
        # reduce camels
        usable_camel_count = max(market_observation.hand_limit - len(hand_goods), 0)
        camels = camels[:usable_camel_count]
        
        max_trade_size = min(
            len(hand_goods) + len(camels), len(market_observation.goods),
        )
        for size in range(1, max_trade_size + 1):
            requested_combos = list(combinations(market_observation.goods, size))
            offered_pool = hand_goods + camels
            offered_combos = list(combinations(offered_pool, size))

            for offered in offered_combos:
                for requested in requested_combos:
                    action = Trade(list(offered), list(requested))
                    if action._is_legal():
                        actions.append(action)
        return actions

    def summary(self):
        """Returns a string representation of the Trade action."""
        return f"Trade(offered={self.offered}, requested={self.requested})"
        
    def __repr__(self):
        return self.summary()
        
    def __str__(self):
        return self.summary()
        
    def __eq__(self, other):
        # two Trade actions are equal the goods requested and offered are the same
        if isinstance(other, Trade):
            return (self.requested == other.requested
                and self.offered == other.offered)
            
    def __hash__(self):
        return hash(self.requested) + hash(self.offered)