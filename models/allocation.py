from typing import Optional

from pydantic import BaseModel
from sqlalchemy_utils import CurrencyType

from pydantic import BaseModel

from tables import AllocatedPieItemModel, AllocationType


class AllocatedPieItemSchema(BaseModel):
    id: int
    type: AllocationType
    title: str
    currency: str
    allocation_in_portfolio: int
    allocation_in_category: int
    asset_ticker: Optional[str]
    exchange_code: Optional[str]
    currency_ticker: Optional[str]
    parent: 'AllocatedPieItemSchema'

    class Config:
        orm_mode = True
