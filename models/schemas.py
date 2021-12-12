from typing import Optional
from pydantic import BaseModel
from models.enums import AllocationType


class PortfolioAllocatedPieSliceBase(BaseModel):
    type: AllocationType
    title: str
    currency: str

    portfolio_id: int
    portfolio_ratio: int

    category_ratio: int

    asset_ticker: Optional[str]
    exchange_code: Optional[str]

    parent_id: Optional[int]

    class Config:
        orm_mode = True


class PortfolioAllocatedPieSliceGet(PortfolioAllocatedPieSliceBase):
    id: int


class PortfolioAllocatedPieSliceCreate(PortfolioAllocatedPieSliceBase):
    pass


class PortfolioAllocatedPieSliceUpdate(PortfolioAllocatedPieSliceBase):
    pass


class PortfolioAllocatedPieSliceDelete(PortfolioAllocatedPieSliceBase):
    pass
