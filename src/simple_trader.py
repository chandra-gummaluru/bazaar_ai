import random
from bazaar_ai.trader import Trader
from bazaar_ai.goods import GoodType

class RuleTrader(Trader):
    """
    Deterministic, hard-coded Bazaar agent.
    Strategy:
      1. Sell high-value goods early
      2. Prefer bonus-triggering sells
      3. Buy only high-value goods
      4. Avoid inventory overflow
    """

    def select_action(self, actions, observation, simulate_action_fnc):

        market_coins = observation.market_goods_coins
        actor_goods = observation.actor_goods
        max_goods = observation.max_player_goods_count
        current_goods = observation.actor_non_camel_goods_count

        # ---------- helper ----------
        def top_coin(good):
            coins = market_coins.get(good, [])
            return coins[-1] if coins else 0

        # ---------- 1. SELL ----------
        sell_actions = []
        for act in actions:
            if act.type == "SELL":
                good = act.good_type
                count = act.count
                value = top_coin(good)

                # bonus incentive
                bonus_weight = 3 if count >= 3 else 0

                sell_score = value * count + bonus_weight
                sell_actions.append((sell_score, act))

        if sell_actions:
            sell_actions.sort(key=lambda x: x[0], reverse=True)
            return sell_actions[0][1]

        # ---------- 2. INVENTORY PRESSURE ----------
        if current_goods >= max_goods - 1:
            # force a sell if possible
            forced_sells = [a for a in actions if a.type == "SELL"]
            if forced_sells:
                return forced_sells[0]

        # ---------- 3. BUY ----------
        buy_actions = []
        for act in actions:
            if act.type == "BUY":
                good = act.good_type
                value = top_coin(good)

                if value >= 4:  # hard-coded threshold
                    buy_actions.append((value, act))

        if buy_actions and current_goods < max_goods:
            buy_actions.sort(key=lambda x: x[0], reverse=True)
            return buy_actions[0][1]

        # ---------- 4. FALLBACK ----------
        # Prefer PASS over random chaos
        for act in actions:
            if act.type == "PASS":
                return act

        return random.choice(actions)
