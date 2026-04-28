from pydantic import BaseModel
from typing import Literal


class CreateWalletRequest(BaseModel):
    name: str
    role: Literal["treasury", "operational", "vendor"]
    asset: str = "BILS"
    initial_balance: float = 0


class TransactionRequest(BaseModel):
    from_wallet_id: str
    to_address: str
    amount: float
    asset: str = "BILS"