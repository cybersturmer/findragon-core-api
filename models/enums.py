from enum import Enum, auto


class AllocationType(Enum):
    ASSET = auto()
    CATEGORY = auto()
    CURRENCY = auto()


class TransactionType(Enum):
    BUY = auto()
    SELL = auto()
    DIVIDENDS = auto()
    COUPON = auto()


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
