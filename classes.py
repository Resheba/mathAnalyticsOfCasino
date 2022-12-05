from pydantic import BaseModel 
from typing import Optional, List, Dict

class Bet(BaseModel):
    user_gave: float
    site_gave: float = 0

    profit: Optional[float]
    is_won: Optional[bool]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.profit = self.site_gave - self.user_gave
        if self.user_gave:
            self.is_won = True if self.site_gave else False
        else: self.is_won = None


class Lot(BaseModel):
    id: int
    ratio: float
    bets: List[Bet]
    
    users_amount: Optional[int]
    site_profit: Optional[float]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.users_amount = len(self.bets)
        self.site_profit = -sum((bet.profit for bet in self.bets))
        del self.bets



