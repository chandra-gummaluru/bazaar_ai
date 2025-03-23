class Coin:
    def __init__(self, good_type, value):
      self._good_type = good_type
      self._value = value

    @property
    def good_type(self):
      return self._good_type

    @property
    def value(self):
      return self._value
      
    def summary(self):
      return f"{self.value}"  

    def __repr__(self):
        return self.summary()
        
    def __str__(self):
        return self.summary()
        
    def __eq__(self, other):
        # two coins are equal if they are the same type and value
        if isinstance(other, BonusCoin):
            return (self.value == other.value and
                self.good_type == other.good_type)
        return False
        
    def __hash__(self):
        return hash(self.good_type) + hash(self.value)
      
      
class BonusCoin:
    def __init__(self, bonus_type, value):
      self._bonus_type = bonus_type
      self._value = value

    @property
    def bonus_type(self):
      return self._bonus_type

    @property
    def value(self):
      return self._value

    def summary(self):
      return f"{self.value}"  
    
    def __repr__(self):
        return self.summary()
        
    def __str__(self):
        return self.summary()
        
    def __eq__(self, other):
        # two bonus coins are equal if they are the same type and value
        if isinstance(other, BonusCoin):
            return (self.value == other.value and
                self.bonus_type == other.bonus_type)
        return False
        
    def __hash__(self):
        return hash(self.bonus_type) + hash(self.value)
        
       