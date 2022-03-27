from pathlib import Path

from app.parser import _csv_lines_to_dicts, csv_to_ledger_entities
from app.io import read_ledger


if __name__ == "__main__":
    path = Path("/home/andreas/administration/bitcoin/kraken/ledgers.csv")

    lines = read_ledger(path)
    entities = csv_to_ledger_entities(lines)

    print(entities)
