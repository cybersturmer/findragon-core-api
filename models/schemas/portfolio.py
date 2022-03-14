from datetime import (
    datetime
)

from pydantic import (
    BaseModel,
    constr
)


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