from datetime import (
    date,
    datetime
)
from typing import (
    Optional
)

from pydantic import (
    BaseModel,
    conint,
    confloat
)

from models import enums
from models.schemas.asset import AssetShort


class IncomeBase(BaseModel):
    operation: enums.IncomeOperationType

    date: date

    amount: confloat(
        ge=0.0
    )

    price: confloat(
        ge=0.0
    )

    tax: confloat(
        ge=0.0
    )

    description: str

    currency: enums.Currency

    portfolio_id: int

    class Config:
        orm_mode = True


class IncomeGet(IncomeBase):
    id:  int

    asset: Optional['AssetShort']

    created_at: datetime
    updated_at: datetime

    def currency_code(self) -> str:
        return self.currency.code


class IncomeCreate(IncomeBase):
    ticker: str
    exchange: str


class IncomeUpdate(IncomeCreate):
    pass
