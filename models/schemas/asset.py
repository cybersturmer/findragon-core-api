from datetime import (
    datetime
)
from typing import (
    Optional
)

from pydantic import (
    BaseModel,
    validator
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

    amount_change: int

    cost_change: Optional[float]

    avg_price: Optional[float]

    @validator(
        'avg_price',
        'cost_change'
    )
    def result_check(cls, v):
        if v is None:
            return v

        return round(v, 2)


class AssetCreate(AssetBase):
    pass