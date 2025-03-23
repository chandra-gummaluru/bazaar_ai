from enum import Enum

class GoodTypes(Enum):
    DIAMOND = "💎"
    GOLD = "🪙"
    SILVER = "🪨"
    FABRIC = "👚"
    SPICE = "🌶️"
    LEATHER = "👞"
    CAMEL = "🐪"
    
class ActionTypes(Enum):
    TAKE    = "take"
    HERD    = "herd"
    SELL    = "sell"
    TRADE   = "trade"
    
class BonusTypes(Enum):
    THREE = "3️⃣"
    FOUR = "4️⃣"
    FIVE = "5️⃣"
    
class Stats(Enum):
    MONEY = "💰"