import unittest
from collections import deque

from parameterized import parameterized

from app.models import Transaction
from app.portfolio import sell


class TestSell(unittest.TestCase):

    @parameterized.expand(
        [
            (30.0, 100.0),
            (40.0, 200.0),
        ]
    )
    def test_sell_all(self, sell_unit_price, expected_profit):
        # Arrange
        transaction1 = Transaction(amount=10.0, unit_price=20.0)
        transaction2 = Transaction(amount=-10.0, unit_price=sell_unit_price)
        asset_queue = deque()
        asset_queue.append(transaction1)

        # Act
        updated_queue, profit, loss = sell(asset_queue, transaction2)

        # Assert
        assert len(updated_queue) == 0
        assert expected_profit == profit

    def test_sell_amount_smaller_than_one_transaction(self):
        # Arrange
        transaction1 = Transaction(amount=10.0, unit_price=20.0)
        transaction2 = Transaction(amount=-7.0, unit_price=30.0)
        asset_queue = deque()
        asset_queue.append(transaction1)

        # Act
        updated_queue, profit, loss = sell(asset_queue, transaction2)

        # Assert
        assert len(updated_queue) == 1
        assert updated_queue.popleft() == Transaction(amount=3.0, unit_price=20.0)
        assert profit == 70.0

    def test_sell_amount_larger_than_one_transaction(self):
        # Arrange
        transaction1 = Transaction(amount=10.0, unit_price=20.0)
        transaction2 = Transaction(amount=20.0, unit_price=30.0)
        transaction3 = Transaction(amount=-15.0, unit_price=40.0)
        asset_queue = deque()
        asset_queue.append(transaction1)
        asset_queue.append(transaction2)

        # Act
        updated_queue, profit, loss = sell(asset_queue, transaction3)

        # Assert
        assert len(updated_queue) == 1
        assert updated_queue.popleft() == Transaction(amount=15.0, unit_price=30.0)
        assert profit == 250.0

    def test_sell_amount_larger_than_two_transactions(self):
        # Arrange
        transaction1 = Transaction(amount=10.0, unit_price=20.0)
        transaction2 = Transaction(amount=10.0, unit_price=30.0)
        transaction3 = Transaction(amount=15.0, unit_price=40.0)
        transaction4 = Transaction(amount=-30.0, unit_price=50.0)
        asset_queue = deque()
        asset_queue.append(transaction1)
        asset_queue.append(transaction2)
        asset_queue.append(transaction3)

        # Act
        updated_queue, profit, loss = sell(asset_queue, transaction4)

        # Assert
        assert len(updated_queue) == 1
        assert updated_queue.popleft() == Transaction(amount=5.0, unit_price=40.0)
        assert profit == 600.0

    def test_sell_all_with_loss(self):
        # Arrange
        transaction1 = Transaction(amount=10.0, unit_price=20.0)
        transaction2 = Transaction(amount=-10.0, unit_price=15.0)
        asset_queue = deque()
        asset_queue.append(transaction1)

        # Act
        updated_queue, profit, loss = sell(asset_queue, transaction2)

        # Assert
        assert len(updated_queue) == 0
        assert profit == 0
        assert loss == 50.0
