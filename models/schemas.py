from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr, conint
from models.enums import AllocationType, BrokerType, PortfolioGoalType


class PortfolioBase(BaseModel):
    id: Optional[int]
    title: constr(min_length=1)

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
    title: constr(min_length=1)

    portfolio_id: Optional[int] = None

    portfolio_ratio: conint(ge=0, le=100)
    category_ratio: conint(ge=0, le=100)

    asset_ticker: Optional[constr(min_length=1)]
    exchange_code: Optional[constr(min_length=1)]

    parent_id: Optional[int]

    class Config:
        orm_mode = True


class PortfolioAllocatedPieSliceGet(PortfolioAllocatedPieSliceBase):
    id: int


class PortfolioAllocatedPieSliceCreate(PortfolioAllocatedPieSliceBase):
    pass


class PortfolioAllocatedPieSliceUpdate(BaseModel):
    title: Optional[constr(min_length=1)]

    portfolio_ratio: Optional[conint(ge=0, le=100)]
    category_ratio: Optional[conint(ge=0, le=100)]


class PortfolioAllocatedPieSliceDelete(PortfolioAllocatedPieSliceBase):
    pass
