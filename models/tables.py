from datetime import datetime, date

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Unicode,
    Date,
    Float,
    DateTime
)

from sqlalchemy.orm import relationship, backref

from sqlalchemy_utils.types import ChoiceType, CurrencyType, EmailType

from database import Base
from models.enums import (
    AllocationType,
    AssetType,
    TransactionType,
    IncomeOperationType
)


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


def portfolio_asset_description_by_default(ctx):
    ticker = ctx.get_current_parameters()["ticker"]
    exchange = ctx.get_current_parameters()["exchange"]

    return f'{ticker}.{exchange}'


class PortfolioAsset(Base):
    __tablename__ = 'portfolio_assets'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    ticker = Column(
        String,
        nullable=False
    )

    exchange = Column(
        String,
        nullable=False
    )

    portfolio_id = Column(
        Integer,
        ForeignKey('portfolio.id')
    )

    portfolio = relationship(
        Portfolio,
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


class PortfolioAssetBaseCache(Base):
    """
    This model helps us to cache information
    that we collect from third party tools.
    It also helps to override information
    from third party tools.
    """

    __tablename__ = 'portfolio_asset_base_cache'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    # Manual data shouldn't be updated,
    # Based on third party tools information
    manual = Column(
        Boolean
    )

    title = Column(
        Unicode(255)
    )

    description = Column(
        Unicode(255)
    )

    ticker = Column(
        String,
        nullable=False
    )

    exchange = Column(
        String,
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
        return f'PortfolioAsset {self.ticker}.{self.exchange}'


class PortfolioAllocation(Base):
    __tablename__ = "portfolio_allocations"

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
        backref=backref('allocations'),
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
        nullable=True
    )

    asset = relationship(
        PortfolioAsset,
        backref=backref('allocations'),
        order_by=id
    )

    parent_id = Column(
        Integer,
        ForeignKey('portfolio_allocations.id'),
        nullable=True
    )

    children = relationship(
        'PortfolioAllocation',
        backref=backref('parent', remote_side=[id])
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
        return f'PortfolioAllocation {self.title} - {self.allocation_in_category}'


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


class PortfolioIncome(Base):
    __tablename__ = 'portfolio_incomes'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    asset_id = Column(
        Integer,
        ForeignKey('portfolio_assets.id'),
        nullable=False
    )

    asset = relationship(
        PortfolioAsset,
        backref=backref('asset_income'),
        order_by=id
    )

    portfolio_id = Column(
        Integer,
        ForeignKey('portfolio.id'),
        nullable=False
    )

    portfolio = relationship(
        Portfolio,
        backref=backref('incomes'),
        order_by=id
    )

    operation = Column(
        ChoiceType(IncomeOperationType, impl=Integer())
    )

    date = Column(
        Date,
        nullable=False,
        default=date.today()
    )

    currency = Column(
        CurrencyType,
        nullable=False
    )

    amount = Column(
        Integer,
        default=1
    )

    price = Column(
        Float,
        default=1
    )

    tax = Column(
        Float,
        default=0.00
    )

    description = Column(
        Unicode(255),
        default=''
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
        return f'PortfolioIncome {self.id} - {IncomeOperationType(self.operation).name} - {self.ticker}'


def portfolio_transaction_amount_change_by_default(ctx):
    type_ = ctx.get_current_parameters()['type']
    amount = ctx.get_current_parameters()['amount']

    return amount * -1 if type_ == TransactionType.SELL else amount


def portfolio_transaction_cost_change_by_default(ctx):
    type_ = ctx.get_current_parameters()['type']
    cost = ctx.get_current_parameters()['cost']

    return cost * -1 if type_ == TransactionType.SELL else cost


class PortfolioTransaction(Base):
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

    # We use it to calculate how this transaction affected balance
    # -x for selling and +x for buying
    amount_change = Column(
        Integer,
        default=portfolio_transaction_amount_change_by_default,
        onupdate=portfolio_transaction_amount_change_by_default
    )

    asset_type = Column(
        ChoiceType(AssetType, impl=Integer())
    )

    # Imported or manually added
    imported = Column(
        Boolean,
        default=False
    )

    import_id = Column(
        Integer,
        ForeignKey('portfolio_imports.id'),
        nullable=True
    )

    # Commission information
    commission = Column(
        Float,
        default=0.00
    )

    currency = Column(
        CurrencyType,
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

    # Only for bonds
    accrued_interest = Column(
        Float,
        nullable=True
    )

    asset_id = Column(
        Integer,
        ForeignKey('portfolio_assets.id'),
        nullable=False
    )

    asset = relationship(
        PortfolioAsset,
        backref=backref('asset_allocation'),
        order_by=id
    )

    # Price per lot and total
    price = Column(
        Float,
        nullable=False
    )

    cost = Column(
        Float,
        nullable=False
    )

    cost_change = Column(
        Float,
        default=portfolio_transaction_cost_change_by_default,
        onupdate=portfolio_transaction_cost_change_by_default
    )

    type = Column(
        ChoiceType(TransactionType, impl=Integer())
    )

    # Portfolio assignment
    portfolio_id = Column(
        Integer, ForeignKey('portfolio.id')
    )

    portfolio = relationship(
        Portfolio,
        backref=backref('portfolio_transactions'),
        order_by=id
    )

    # Date of the transaction
    date = Column(
        Date,
        nullable=False,
        default=date.today()
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
