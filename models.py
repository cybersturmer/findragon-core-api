from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Unicode
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy_utils import Currency, CurrencyType

from database import Base
from enum import Enum, auto


class AllocationType(Enum):
    ASSET = auto()
    CATEGORY = auto()
    CURRENCY = auto()


class AllocatedPieItemModel(Base):
    __tablename__ = "allocated_pie_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    type = Column(
        ChoiceType(AllocationType, impl=Integer())
    )

    title = Column(
        Unicode(255),
        nullable=True
    )

    currency = Column(
        CurrencyType
    )

    allocation_in_portfolio = Column(
        Integer
    )

    allocation_in_category = Column(
        Integer
    )

    asset_ticker = Column(
        String,
        nullable=True
    )

    exchange_code = Column(
        String,
        nullable=True
    )

    currency_ticker = Column(
        String,
        nullable=True
    )

    parent = Column(
        Integer,
        ForeignKey('allocated_pie_items.id')
    )


