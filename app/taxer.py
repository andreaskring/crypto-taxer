from itertools import groupby
from pathlib import Path
from pprint import pprint

from app.parser import _csv_lines_to_dicts, csv_to_ledger_entities, get_asset_types
from app.io import read_ledger
from app.portfolio import process_portfolio

if __name__ == "__main__":
    path = Path("/home/andreas/administration/bitcoin/kraken/ledgers.csv")

    lines = read_ledger(path)
    entities = csv_to_ledger_entities(lines)
    # print(entities)

    g = groupby(entities, lambda entity: entity.refid)
    l = [list(g) for k, g in g]

    assets = get_asset_types(entities)
    # print(assets)

    p, profit, loss = process_portfolio(l, assets)
    pprint(p)
    print("profit:", profit)
    print("loss:", loss)
