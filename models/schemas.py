from typing import Optional
from pydantic import BaseModel
from models.enums import AllocationType


class PortfolioAllocatedPieSlice(BaseModel):
    id: int
    type: AllocationType
    title: str
    currency: str

    portfolio_id: int
    portfolio_ratio: int

    category_ratio: int

    asset_ticker: Optional[str]
    exchange_code: Optional[str]
    currency_ticker: Optional[str]

    parent: int

    class Config:
        orm_mode = True
