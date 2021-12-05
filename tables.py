from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Unicode, Date, Float
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy_utils import Currency, CurrencyType

from database import Base
from enum import Enum, auto


class AllocationType(Enum):
    ASSET = auto()
    CATEGORY = auto()
    CURRENCY = auto()


class TransactionType(Enum):
    BUY = auto()
    SELL = auto()


class BrokerType(Enum):
    SBER = auto()
    TCS = auto()


class PortfolioGoalType(Enum):
    GROW = auto()
    INCOME = auto()


class PaymentType(Enum):
    DIVIDENDS = auto()
    COUPON = auto()


class AssetType(Enum):
    SHARE = auto()
    BOND = auto()
    FUND = auto()


class PortfolioSettingsModel(Base):
    __tablename__ = 'portfolio_settings'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    apply_taxes_on_paid_dividends = Column(
        Boolean
    )

    tax_percent = Column(
        Integer
    )

    broker = Column(
        ChoiceType(BrokerType, impl=Integer())
    )

    goal_currency = Column(
        String
    )

    goal_type = Column(
        ChoiceType(PortfolioGoalType, impl=Integer())
    )

    goal_value = Column(
        Integer
    )


class AllocatedPieItemModel(Base):
    __tablename__ = "allocated_pie_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    type = Column(
        ChoiceType(AllocationType, impl=Integer())
    )

    title = Column(
        Unicode(255),
        nullable=True
    )

    currency = Column(
        String
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

    parent = Column(
        Integer,
        ForeignKey('allocated_pie_items.id')
    )


class PortfolioTransactionModel(Base):
    __tablename__ = 'portfolio_transactions'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    amount = Column(
        Integer
    )

    asset_type = Column(
        ChoiceType(AssetType, impl=Integer())
    )

    imported = Column(
        Boolean
    )

    commission = Column(
        Float
    )

    commission_currency = Column(
        String
    )

    date = Column(
        Date
    )

    description = Column(
        Unicode(255)
    )

    title = Column(
        Unicode(55)
    )

    accrued_interest = Column(
        Float
    )

    price = Column(
        Float
    )

    ticker = Column(
        String
    )

    exchange = Column(
        String
    )

    total_price = Column(
        Float
    )

    type = Column(
        ChoiceType(TransactionType, impl=Integer())
    )


class InvestmentModel(Base):
    __tablename__ = 'portfolio_investment'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    amount = Column(
        Float
    )

    buy_value = Column(
        Float
    )

    currency = Column(
        String
    )

    description = Column(
        Unicode(255)
    )

    exchange = Column(
        String
    )

    ticker = Column(
        String
    )
