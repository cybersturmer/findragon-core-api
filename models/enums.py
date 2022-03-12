from enum import Enum, auto


class AllocationType(Enum):
    ASSET = auto()
    CATEGORY = auto()
    CURRENCY = auto()


class TransactionType(Enum):
    BUY = auto()
    SELL = auto()


class IncomeOperationType(Enum):
    DIVIDENDS = auto()  # Dividends paid by money
    SHARES = auto()     # Dividends paid by shares
    COUPONS = auto()    # Coupons paid for bonds
    OTHER = auto()


class BrokerType(Enum):
    SBER = auto()
    INTERACTIVE_BROKERS = auto()
    FREEDOM_FINANCE = auto()
    ATON = auto()
    JUST2TRADE = auto()
    VANGUARD = auto()
    TINKOFF = auto()
    BKS = auto()
    OTKRITIE = auto()
    TD_AMERITRADE = auto()
    WEBULL = auto()
    VTB = auto()
    FINAM = auto()
    ALFA = auto()
    EXANTE = auto()
    ROBINHOOD = auto()


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


class Currency(Enum):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    AUD = 'AUD'
    CAD = 'CAD'
    CHF = 'CHF'
    CNY = 'CNY'
    CZK = 'CZK'
    GBP = 'GBP'
    HKD = 'HKD'
    ILS = 'ILS'
    JPY = 'JPY'
    KZT = 'KZT'
    PLN = 'PLN'
    SEK = 'SEK'
    SGD = 'SGD'
    TRY = 'TRY'
    UAH = 'UAH'
