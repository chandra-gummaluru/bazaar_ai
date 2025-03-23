from ..terms import GoodTypes

class Good:
    def __init__(self, good_type):
        self._good_type = good_type

    @property
    def good_type(self):
        return self._good_type
    
    def summary(self):
      return self.good_type.value
      
    def __repr__(self):
      return self.summary()
      
    def __str__(self):
        return self.summary()
        
    def __eq__(self, other):
        # two goods are equal if they are the same type
        if isinstance(other, Good):
            return self.good_type == other.good_type
        return False
            
    def __hash__(self):
        return hash(self.good_type)