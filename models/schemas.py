from datetime import date, datetime
from typing import Optional, List, ForwardRef, Dict
from pydantic import BaseModel, constr, conint, confloat, validator
from sqlalchemy_utils import CurrencyType, Currency

from models import enums


class PortfolioBase(BaseModel):
    title: constr(
        strip_whitespace=True,
        min_length=1
    )

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


class AssetCreate(AssetBase):
    pass


class TransactionBase(BaseModel):
    amount: conint(ge=1)

    asset_type: enums.AssetType

    commission: confloat(ge=0.0)

    description: str = ''
    title: str = ''

    accrued_interest: Optional[float]  # For bonds only

    price: confloat(ge=0.0)

    type: enums.TransactionType

    date: date

    portfolio_id: int

    class Config:
        orm_mode = True


class TransactionGet(TransactionBase):
    id: int

    imported: bool = False
    import_id: Optional[int] = None

    total_price: int

    @property
    def currency_code(self) -> str:
        return self.currency.code

    created_at: datetime
    updated_at: datetime


class TransactionCreate(TransactionBase):
    ticker: str
    exchange: str

    currency: str


class TransactionsImportResult(AssetBase):
    commissions_amount: conint(ge=0)
    dividends_amount: conint(ge=0)
    transactions_amount: conint(ge=0)

    assets_affected: conint(ge=0)

    messages: List[Dict[str, str]]

    success: bool
