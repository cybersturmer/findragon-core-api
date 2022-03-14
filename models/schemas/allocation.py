from typing import (
    Optional,
    List
)

from pydantic import (
    BaseModel,
    constr,
    conint
)

from models import enums
from models.schemas.asset import AssetShort


class PortfolioAllocationBase(BaseModel):
    type: enums.AllocationType
    title: constr(
        strip_whitespace=True,
        min_length=1
    )

    portfolio_id: Optional[int] = None

    category_ratio: conint(
        ge=100,
        le=10000
    )

    parent_id: Optional[int]

    class Config:
        orm_mode = True


class PortfolioAllocationGet(PortfolioAllocationBase):
    id: int
    portfolio_ratio: conint(ge=1, le=10000)

    asset: Optional['AssetShort']

    children: List['PortfolioAllocationGet']


PortfolioAllocationGet.update_forward_refs()


class PortfolioAllocationCreate(PortfolioAllocationBase):
    ticker: Optional[
        constr(min_length=1)
    ]

    exchange: Optional[
        constr(min_length=1)
    ]


class PortfolioAllocationUpdate(BaseModel):
    category_ratio: Optional[conint(ge=100, le=10000)]


class PortfolioAllocationDelete(PortfolioAllocationBase):
    pass