from arelai.game import State, Observation

from .goods import GoodType, Goods
from .coins import BonusType, Coins

import random
from uuid import UUID


class Market(State):
   
    def __init__(
        self,
        seed,
        player_ids: list[UUID],
        actor_id: UUID,
        reserved_goods: list[GoodType],
        goods_coins: dict[GoodType, list],
        bonus_coins: dict[BonusType, list],
        camel_bonus: int,
        max_goods_count: int,
        max_player_goods_count: int,
        initial_player_goods_count: int,
    ):
        
        super().__init__(
            actor_ids=[actor_id])

        # use this for random operations
        self.rng = random.Random(seed)

        self.player_ids = player_ids

        self.reserved_goods = reserved_goods
        self.rng.shuffle(self.reserved_goods)

        self.coins = Coins()
        for good_type in goods_coins.keys():
            for coin in goods_coins[good_type]:
                self.coins.add_goods_coin(good_type, coin)
        for bonus_type in bonus_coins.keys():
            for coin in bonus_coins[bonus_type]:
                self.coins.add_bonus_coin(bonus_type, coin)

        self.player_goods = {}
        self.player_coins = {}
        
        for player_id in self.player_ids:
            self.player_coins[player_id] = Coins()
            self.player_goods[player_id] = Goods()

        self.max_player_goods_count = max_player_goods_count
        self.initial_player_goods_count = initial_player_goods_count
        
        # give each player some goods
        for _ in range(initial_player_goods_count):
            for player_id in self.player_ids:
                good_type = self.reserved_goods.pop()
                self.player_goods[player_id].add(good_type)

        self.max_goods_count = max_goods_count
        self.goods = Goods()
        self.refill_market()

        self.sold_goods = []

        self.camel_bonus = camel_bonus
        self.max_goods_count = max_goods_count
    
    def refill_market(self):
        while self.goods.count() < self.max_goods_count:
            if self.reserved_goods:
                good_type = self.reserved_goods.pop()
                self.goods.add(good_type)

    def get_non_actor(self):
        non_actor_id = [player_id for player_id in self.player_ids if
                               player_id not in self.actor_ids][0]
        return non_actor_id


class MarketObservation(Observation):
    def __init__(self,
            observer_id: UUID,
            actor_id: UUID,
            actor_goods: Goods,
            actor_goods_coins: dict[GoodType, list[int]],
            actor_bonus_coins_counts: dict[BonusType, int],
            market_goods: Goods,
            market_goods_coins: dict[GoodType, list[int]],
            market_bonus_coins_counts: dict[BonusType, int],
            market_reserved_goods_count: int,
            max_player_goods_count: int,
            max_market_goods_count: int
    ):
        self.actor = actor_id
        self.actor_goods = actor_goods
        self.actor_goods_coins = actor_goods_coins
        self.actor_bonus_coins_counts = actor_bonus_coins_counts
        self.market_goods = market_goods
        self.market_goods_coins = market_goods_coins
        self.market_bonus_coins_counts = market_bonus_coins_counts
        self.market_reserved_goods_count = market_reserved_goods_count
        self.max_player_goods_count = max_player_goods_count
        self.max_market_goods_count = max_market_goods_count

        self.actor_non_camel_goods_count = self.actor_goods.count(include_camels=False)

        super().__init__(observer_id)
    
