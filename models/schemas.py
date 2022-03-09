from datetime import date, datetime
from typing import Optional, List, Dict

from pydantic import BaseModel, constr, conint, confloat

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


class AssetCreate(AssetBase):
    pass


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

    ticker: Optional[
        constr(min_length=1)
    ]

    exchange: Optional[
        constr(min_length=1)
    ]

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
    title: Optional[constr(min_length=1)]

    portfolio_ratio: Optional[conint(ge=1, le=10000)]
    category_ratio: Optional[conint(ge=100, le=10000)]


class PortfolioAllocationDelete(PortfolioAllocationBase):
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

    asset: Optional['AssetShort']

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


class TransactionUpdate(TransactionCreate):
    pass


class TransactionsImportResult(AssetBase):
    commissions_amount: conint(ge=0)
    dividends_amount: conint(ge=0)
    transactions_amount: conint(ge=0)

    assets_affected: conint(ge=0)

    messages: List[Dict[str, str]]

    success: bool
