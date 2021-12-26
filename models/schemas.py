from datetime import datetime
from typing import Optional, List, ForwardRef
from pydantic import BaseModel, constr, conint, confloat, validator
from sqlalchemy_utils import CurrencyType, Currency

from models.enums import AllocationType, BrokerType, PortfolioGoalType


class PortfolioBase(BaseModel):
    title: constr(
        strip_whitespace=True,
        min_length=1
    )

    apply_taxes_on_income: bool

    tax_percent: conint(ge=0, le=100)

    broker: BrokerType

    goal_currency: str
    goal_type: PortfolioGoalType
    goal_value: int

    class Config:
        orm_mode = True


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioGet(PortfolioBase):
    id: int
    created_at: datetime
    updated_at: datetime


class PortfolioUpdate(PortfolioGet):
    pass


class PortfolioDelete(PortfolioBase):
    pass


class PortfolioAllocatedPieSliceBase(BaseModel):
    type: AllocationType
    title: constr(
        strip_whitespace=True,
        min_length=1
    )

    portfolio_id: Optional[int] = None

    category_ratio: conint(
        ge=100,
        le=10000
    )

    asset_ticker: Optional[
        constr(min_length=1)
    ]

    exchange_code: Optional[
        constr(min_length=1)
    ]

    parent_id: Optional[int]

    class Config:
        orm_mode = True


class PortfolioAllocatedPieSliceGet(PortfolioAllocatedPieSliceBase):
    id: int
    portfolio_ratio: conint(ge=100, le=10000)
    children: List['PortfolioAllocatedPieSliceGet']


PortfolioAllocatedPieSliceGet.update_forward_refs()


class PortfolioAllocatedPieSliceCreate(PortfolioAllocatedPieSliceBase):
    pass


class PortfolioAllocatedPieSliceUpdate(BaseModel):
    title: Optional[constr(min_length=1)]

    portfolio_ratio: Optional[conint(ge=100, le=10000)]
    category_ratio: Optional[conint(ge=100, le=10000)]


class PortfolioAllocatedPieSliceDelete(PortfolioAllocatedPieSliceBase):
    pass


class AssetBase(BaseModel):
    amount: conint(gt=1)

    price: confloat(gt=0.0)

    description: str

    exchange: str
    ticker: str

    portfolio_id: int

    class Config:
        orm_mode = True


class AssetGet(AssetBase):
    id: int

    currency_code: str
    currency_symbol: str

    created_at: datetime
    updated_at: datetime


class AssetCreate(AssetBase):
    currency: str
