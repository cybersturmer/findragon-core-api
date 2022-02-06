from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Unicode, Date, Float, DateTime
from sqlalchemy.orm import relationship, backref

from sqlalchemy_utils.types import ChoiceType, CurrencyType, EmailType

from database import Base
from models.enums import \
    BrokerType, \
    PortfolioGoalType, \
    AllocationType, \
    AssetType, \
    TransactionType


class User(Base):
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
        EmailType,
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


class Portfolio(Base):
    __tablename__ = 'portfolio'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    title = Column(
        Unicode(255),
        nullable=False
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
        CurrencyType,
        nullable=True
    )

    @property
    def goal_currency_code(self) -> str:
        return self.goal_currency.code

    @property
    def goal_currency_name(self) -> str:
        return self.goal_currency.name

    @property
    def goal_currency_symbol(self) -> str:
        return self.goal_currency.symbol

    goal_type = Column(
        ChoiceType(PortfolioGoalType, impl=Integer()),
        nullable=True
    )

    goal_value = Column(
        Integer,
        default=0
    )

    user_id = Column(
        Integer,
        ForeignKey('users.id')
    )

    user = relationship(
        User,
        backref=backref('portfolios'),
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
        return f'Portfolio ({self.id})'


class PortfolioAsset(Base):
    __tablename__ = 'portfolio_assets'

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

    price = Column(
        Float,
        nullable=False
    )

    currency = Column(
        CurrencyType,
        nullable=False
    )

    @property
    def currency_code(self) -> str:
        return self.currency.code

    @property
    def currency_name(self) -> str:
        return self.currency.name

    @property
    def currency_symbol(self) -> str:
        return self.currency.symbol

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

    portfolio_id = Column(
        Integer, ForeignKey('portfolio.id')
    )

    portfolio = relationship(
        Portfolio,
        backref=backref('assets'),
        order_by=id
    )

    user_id = Column(
        Integer, ForeignKey('users.id')
    )

    user = relationship(
        User,
        backref=backref('assets'),
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
        return f'PortfolioAsset {self.id} - {self.ticker} / {self.amount} '


class PortfolioAllocatedPieSlice(Base):
    __tablename__ = "portfolio_allocated_pie_slices"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    type = Column(
        ChoiceType(AllocationType, impl=Integer()),
        nullable=False
    )

    title = Column(
        Unicode(255),
        nullable=False
    )

    portfolio_id = Column(
        Integer,
        ForeignKey('portfolio.id'),
        nullable=False
    )

    portfolio = relationship(
        Portfolio,
        backref=backref('allocated_pie_slices'),
        order_by=id
    )

    portfolio_ratio = Column(
        Integer,
        default=0
    )

    category_ratio = Column(
        Integer,
        default=0
    )

    asset_id = Column(
        Integer,
        ForeignKey('portfolio_assets.id'),
        nullable=False
    )

    asset = relationship(
        PortfolioAsset,
        backref=backref('allocations'),
        order_by=id
    )

    parent_id = Column(
        Integer,
        ForeignKey('portfolio_allocated_pie_slices.id'),
        nullable=True
    )

    children = relationship(
        'PortfolioAllocatedPieSlice',
        backref=backref('parent', remote_side=[id])
    )

    user_id = Column(
        Integer, ForeignKey('users.id')
    )

    user = relationship(
        User,
        backref=backref('allocated_pie_slices'),
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
        return f'PortfolioAllocatedPieSlice {self.title} - {self.allocation_in_category}'


class PortfolioImports(Base):
    __tablename__ = 'portfolio_imports'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
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
        return f'PortfolioImport {str(self.created_at)}'


class PortfolioTransaction(Base):
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

    import_id = Column(
        Integer,
        ForeignKey('portfolio_imports.id'),
        nullable=True
    )

    commission = Column(
        Float,
        default=0.00
    )

    commission_currency = Column(
        CurrencyType,
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

    asset_id = Column(
        Integer,
        ForeignKey('portfolio_assets.id'),
        nullable=False
    )

    asset = relationship(
        PortfolioAsset,
        backref=backref('allocations'),
        order_by=id
    )

    total_price = Column(
        Float,
        default=0.00
    )

    type = Column(
        ChoiceType(TransactionType, impl=Integer())
    )

    portfolio_id = Column(
        Integer, ForeignKey('portfolio.id')
    )

    portfolio = relationship(
        Portfolio,
        backref=backref('transactions'),
        order_by=id
    )

    user_id = Column(
        Integer, ForeignKey('users.id')
    )

    user = relationship(
        User,
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
