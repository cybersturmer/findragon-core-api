from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Unicode, Date, Float, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils.types import ChoiceType

from database import Base
from models.enums import \
    BrokerType, \
    PortfolioGoalType, \
    AllocationType, \
    AssetType, \
    TransactionType


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    username = Column(
        String(15),
        nullable=False,
        unique=True
    )

    email = Column(
        String(255),
        nullable=False
    )

    password = Column(
        String(25),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )

    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )

    def __repr__(self):
        return f'User (@{self.username})'


class PortfolioSettingsModel(Base):
    __tablename__ = 'portfolio_settings'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    apply_taxes_on_income = Column(
        Boolean,
        default=False
    )

    tax_percent = Column(
        Integer,
        default=0
    )

    broker = Column(
        ChoiceType(BrokerType, impl=Integer()),
        nullable=False
    )

    goal_currency = Column(
        String,
        nullable=True
    )

    goal_type = Column(
        ChoiceType(PortfolioGoalType, impl=Integer()),
        nullable=True
    )

    goal_value = Column(
        Integer,
        default=0
    )

    user_id = Column(
        Integer, ForeignKey('users.id')
    )

    user = relationship(
        UserModel,
        backref=backref('portfolio_settings'),
        order_by=id
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )

    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )

    def __repr__(self):
        return f'PortfolioSetting ({self.id})'


class PortfolioAllocatedPieItemModel(Base):
    __tablename__ = "portfolio_allocated_pie_items"

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
        String,
        nullable=False
    )

    allocation_in_portfolio = Column(
        Integer,
        default=0
    )

    allocation_in_category = Column(
        Integer,
        default=0
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
        ForeignKey('portfolio_allocated_pie_items.id')
    )

    user_id = Column(
        Integer, ForeignKey('users.id')
    )

    user = relationship(
        UserModel,
        backref=backref('allocated_pies'),
        order_by=id
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )

    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )

    def __repr__(self):
        return f'AllocatedPieItem {self.title} - {self.allocation_in_category}'


class PortfolioTransactionModel(Base):
    __tablename__ = 'portfolio_transactions'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    amount = Column(
        Integer,
        default=0
    )

    asset_type = Column(
        ChoiceType(AssetType, impl=Integer())
    )

    imported = Column(
        Boolean,
        nullable=False
    )

    commission = Column(
        Float,
        default=0.00
    )

    commission_currency = Column(
        String,
        nullable=False
    )

    date = Column(
        Date,
        nullable=False
    )

    description = Column(
        Unicode(255),
        default=''
    )

    title = Column(
        Unicode(55),
        default=''
    )

    accrued_interest = Column(
        Float,
        default=0.00
    )

    price = Column(
        Float,
        default=0.00
    )

    ticker = Column(
        String,
        nullable=False
    )

    exchange = Column(
        String,
        nullable=False
    )

    total_price = Column(
        Float,
        default=0.00
    )

    type = Column(
        ChoiceType(TransactionType, impl=Integer())
    )

    user_id = Column(
        Integer, ForeignKey('users.id')
    )

    user = relationship(
        UserModel,
        backref=backref('transactions'),
        order_by=id
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )

    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )

    def __repr__(self):
        return f'PortfolioTransaction {self.id} - {TransactionType(self.type).name} - {self.ticker}'


class PortfolioInvestmentModel(Base):
    __tablename__ = 'portfolio_investments'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    amount = Column(
        Integer,
        nullable=False
    )

    buy_value = Column(
        Float,
        nullable=False
    )

    currency = Column(
        String,
        nullable=False
    )

    description = Column(
        Unicode(255),
        default=''
    )

    exchange = Column(
        String,
        nullable=False
    )

    ticker = Column(
        String,
        nullable=False
    )

    user_id = Column(
        Integer, ForeignKey('users.id')
    )

    user = relationship(
        UserModel,
        backref=backref('investments'),
        order_by=id
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )

    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )

    def __repr__(self):
        return f'Investment {self.id} - {self.ticker} / {self.amount} '
