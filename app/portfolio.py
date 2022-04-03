from collections import deque
from copy import deepcopy
from itertools import groupby
from typing import List, Tuple, Deque

from app.models import LedgerEntity, Transaction
from app.parser import get_asset_types, EURO_KEYS


def group_by_refid(entities: List[LedgerEntity]) -> List[List[LedgerEntity]]:
    groups = groupby(entities, lambda entity: entity.refid)
    return [list(g) for _, g in groups]


def sell(
    asset_queue: Deque[Transaction],
    sell_transaction: Transaction,
    profit: float = 0.0
) -> Tuple[Deque[Transaction], float]:
    buy_transaction = asset_queue.popleft()
    amount_diff = buy_transaction.amount + sell_transaction.amount
    assert amount_diff >= 0
    profit = (sell_transaction.unit_price - buy_transaction.unit_price) * abs(sell_transaction.amount)

    updated_transaction = Transaction(amount=amount_diff, unit_price=buy_transaction.unit_price)
    if amount_diff > 0:
        asset_queue.appendleft(updated_transaction)

    return asset_queue, profit


def process_portfolio(
    entity_groups: List[List[LedgerEntity]],
    assert_types: Tuple[str]
):
    portfolio = {asset: deque() for asset in assert_types}

    def assets_in_group_different(entity_group) -> bool:
        return not (
            entity_group[0].asset in EURO_KEYS and
            entity_group[1].asset in EURO_KEYS
        )

    egs = filter(assets_in_group_different, entity_groups)
    for eg in egs:
        assert len(eg) == 2, "More than two entities in transaction"
        if eg[0].asset in EURO_KEYS:
            # Buying asset
            coin_amount = eg[1].amount
            unit_price = abs(eg[0].amount) / eg[1].amount
            transaction = Transaction(amount=coin_amount, unit_price=unit_price)

            portfolio[eg[1].asset].append(transaction)
        else:
            # Selling asset
            pass

    return portfolio
