from collections import deque
from itertools import groupby
from pprint import pprint
from typing import List, Tuple, Deque

from app.models import LedgerEntity, Transaction
from app.parser import EURO_KEYS


def group_by_refid(entities: List[LedgerEntity]) -> List[List[LedgerEntity]]:
    groups = groupby(entities, lambda entity: entity.refid)
    return [list(g) for _, g in groups]


def sell(
    asset_queue: Deque[Transaction],
    sell_transaction: Transaction,
) -> Tuple[Deque[Transaction], float, float]:

    amount_left_to_sell = abs(sell_transaction.amount)
    profit = 0
    loss = 0

    while amount_left_to_sell > 0:
        buy_transaction = asset_queue.popleft()
        amount_sold = min(buy_transaction.amount, amount_left_to_sell)

        profit_or_loss = (sell_transaction.unit_price - buy_transaction.unit_price) * amount_sold
        if profit_or_loss >= 0:
            profit += profit_or_loss
        else:
            loss += abs(profit_or_loss)

        amount_left_to_sell -= amount_sold
        if amount_sold < buy_transaction.amount:
            updated_buy_transaction = Transaction(
                amount=buy_transaction.amount - amount_sold,
                unit_price=buy_transaction.unit_price
            )
            asset_queue.appendleft(updated_buy_transaction)

    return asset_queue, profit, loss


def process_portfolio(
    entity_groups: List[List[LedgerEntity]],
    assert_types: Tuple[str]
):
    portfolio = {asset: deque() for asset in assert_types}
    profit = {asset: 0 for asset in assert_types}
    loss = {asset: 0 for asset in assert_types}

    def assets_in_group_different(entity_group) -> bool:
        return not (
            entity_group[0].asset in EURO_KEYS and
            entity_group[1].asset in EURO_KEYS
        )

    egs = filter(assets_in_group_different, entity_groups)
    for eg in egs:
        # pprint(eg)
        assert len(eg) == 2, "More than two entities in transaction"
        if eg[0].asset in EURO_KEYS:
            # Buying asset
            coin_amount = eg[1].amount
            fee = eg[1].fee
            unit_price = abs(eg[0].amount) / eg[1].amount
            transaction = Transaction(amount=coin_amount - fee, unit_price=unit_price)

            portfolio[eg[1].asset].append(transaction)
        else:
            # Selling asset
            asset = eg[0].asset
            coin_amount = eg[0].amount
            unit_price = eg[1].amount / abs(eg[0].amount)
            sell_transaction = Transaction(amount=coin_amount, unit_price=unit_price)
            _, _profit, _loss = sell(portfolio[asset], sell_transaction)
            profit[asset] += _profit
            loss[asset] += _loss

        coin_to_watch = "INJ"
        if eg[0].asset == coin_to_watch or eg[1].asset == coin_to_watch:
            print(30*"-")
            pprint(portfolio)
            print("profit:", profit)
            print("loss:", loss)
            input()

    return portfolio, profit, loss
