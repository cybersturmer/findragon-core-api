from datetime import (
    date,
    datetime
)
from typing import (
    Optional,
    List,
    Dict
)

from pydantic import (
    BaseModel,
    conint,
    confloat
)

from models import enums
from models.schemas.asset import AssetShort, AssetBase


class TransactionBase(BaseModel):
    amount: conint(ge=1)

    asset_type: enums.AssetType

    commission: confloat(ge=0.0)

    description: Optional[str] = ''
    title: Optional[str] = ''

    accrued_interest: Optional[float]  # For bonds only

    price: float

    type: enums.TransactionType

    date: date

    portfolio_id: int

    class Config:
        orm_mode = True


class TransactionGet(TransactionBase):
    id: int

    asset: Optional['AssetShort']

    amount_change: float

    cost: float
    cost_change: float

    imported: bool = False
    import_id: Optional[int] = None

    @property
    def currency_code(self) -> str:
        return self.currency.code

    created_at: datetime
    updated_at: datetime


class TransactionCreate(TransactionBase):
    ticker: str
    exchange: str

    currency: enums.Currency


class TransactionUpdate(TransactionCreate):
    pass


class TransactionsImportResult(AssetBase):
    commissions_amount: conint(ge=0)
    dividends_amount: conint(ge=0)
    transactions_amount: conint(ge=0)

    assets_affected: conint(ge=0)

    messages: List[Dict[str, str]]

    success: bool