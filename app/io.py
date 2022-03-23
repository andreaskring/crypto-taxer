from pathlib import Path
from typing import List


def read_ledger(path: Path) -> List[str]:
    with open(str(path)) as csv:
        lines = csv.readlines()
    return lines
