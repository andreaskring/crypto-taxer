from datetime import datetime
from enum import Enum, auto, unique
from typing import Optional, Any, Dict

from pydantic import BaseModel
from pydantic.fields import Field


@unique
class EntityType(Enum):
    DEPOSIT = 'deposit'
    RECEIVE = 'receive'
    SPEND = 'spend'
    TRADE = 'trade'


class LedgerEntity(BaseModel):
    txid: Optional[str] = None
    refid: Optional[str] = None
    time: datetime
    entity_type: EntityType = Field(..., alias="type")
    subtype: Optional[str] = None
    aclass: Optional[str] = None
    asset: str
    amount: float
    fee: float
    balance: Optional[float] = None


class Transaction(BaseModel):
    amount: float
    unit_price: float
