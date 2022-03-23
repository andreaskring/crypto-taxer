from typing import List, Dict, Any


def _csv_lines_to_dicts(csv: List[str]) -> List[Dict[str, Any]]:
    keys = csv[0].split(",")
    values = map(lambda line: line.split(","), csv[1:])
    dicts = [dict(zip(keys, value)) for value in values]
    return dicts


