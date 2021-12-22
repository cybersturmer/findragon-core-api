from datetime import datetime
from typing import Optional, List, ForwardRef
from pydantic import BaseModel, constr, conint
from models.enums import AllocationType, BrokerType, PortfolioGoalType


class PortfolioBase(BaseModel):
    id: Optional[int]
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

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioGet(PortfolioBase):
    pass


class PortfolioUpdate(PortfolioBase):
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
