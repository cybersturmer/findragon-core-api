from pydantic import (
    BaseModel
)


class DashboardTotalPurchase(BaseModel):
    total_purchase: int
