from pydantic import (
    BaseModel
)


class DashboardTotalPurchase(BaseModel):
    total_purchase: int


class DashboardAssetsStats(BaseModel):
    id: int
    code: str
    price: float
    amount: int

    total_purchase_cost: int
    total_market_price: int

    portfolio_change: float
    portfolio_change_p: float

    change: float
    change_p: float