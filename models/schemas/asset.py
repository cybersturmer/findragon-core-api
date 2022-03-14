from datetime import (
    datetime
)
from typing import (
    Optional
)

from pydantic import (
    BaseModel
)


class AssetBase(BaseModel):
    description: Optional[str] = ''

    exchange: str
    ticker: str

    portfolio_id: int

    class Config:
        orm_mode = True


class AssetGet(AssetBase):
    id: int

    created_at: datetime
    updated_at: datetime


class AssetShort(BaseModel):
    ticker: str
    exchange: str

    description: str

    class Config:
        orm_mode = True


class AssetAggregated(AssetShort):
    id: int

    amount: int

    avg_price: Optional[float]
    total_price: Optional[float]


class AssetCreate(AssetBase):
    pass