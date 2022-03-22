from typing import List

from models import tables
from models.enums import TransactionType


class TransactionsMaster:
    def __init__(
            self,
            transactions: List[tables.PortfolioTransaction],
    ):
        self.__transactions = transactions
        self.__buying_transactions = [
            transaction
            for transaction
            in self.__transactions
            if transaction.type == TransactionType.BUY
        ]

        self.__selling_transactions = [
            transaction
            for transaction
            in self.__transactions
            if transaction.type == TransactionType.SELL
        ]

    def calculate_purchase_amount(self):
        return sum([
            __transaction.amount_change
            for __transaction
            in self.__transactions
        ])

    def calculate_purchase_cost(self, amount: int) -> float:
        reversed_buying_transactions = reversed(self.__buying_transactions)

        _to_process_amount = amount
        _current_purchase_cost = 0

        for _transaction in reversed_buying_transactions:
            _diff = _to_process_amount - _transaction.amount

            if _diff < 0:
                # From the last transaction amount subtract difference and mult on price.
                _current_purchase_cost += (_transaction.amount + _diff) * _transaction.price
                break
            elif _diff == 0:
                _current_purchase_cost += _transaction.cost
                break
            else:
                _current_purchase_cost += _transaction.cost
                _to_process_amount -= _transaction.amount

        return _current_purchase_cost

    def calculate_average_price(self):
        # Calculate diff between buy and sell transactions
        # Positive - We bought more than sell
        # Zero - we sold everything that bought
        # Negative - should be impossible, we can't sell more than have

        amount = self.calculate_purchase_amount()

        assert amount >= 0, \
            'We cant sell more than we have'

        # We cannot calculate average price if we don't have assets
        if amount == 0:
            return None

        purchase_cost = self.calculate_purchase_cost(amount)

        return purchase_cost / amount
