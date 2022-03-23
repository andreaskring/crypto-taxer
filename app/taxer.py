from pathlib import Path

from app.parser import _csv_lines_to_dicts
from app.io import read_ledger


if __name__ == "__main__":
    path = Path("/home/andreas/administration/bitcoin/kraken/ledgers.csv")
    lines = read_ledger(path)

    print(_csv_lines_to_dicts(lines))
