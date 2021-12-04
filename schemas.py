from typing import Optional

from pydantic import BaseModel
from sqlalchemy_utils import CurrencyType

from models import AllocationType


class AllocatedPieItemSchema(BaseModel):
    type: AllocationType
    title: str
    currency: CurrencyType
    allocation_in_portfolio: int
    allocation_in_category: int
    asset_ticker: Optional[str]
    exchange_code: Optional[str]
    currency_ticker: Optional[str]
    parent: 'AllocatedPieItemSchema'
