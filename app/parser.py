from typing import List, Dict, Any


# TODO: use named tuples instead
def _csv_lines_to_dicts(csv: List[str]) -> List[Dict[str, Any]]:
    def remove_quotes(s: str) -> str:
        assert s.count('"') <= 2
        return s.replace('"', '')

    keys = csv[0].split(",")
    keys = list(map(remove_quotes, keys))

    values = map(lambda line: line.split(","), csv[1:])
    values = [map(remove_quotes, value) for value in values]

    dicts = [dict(zip(keys, value)) for value in values]

    return dicts


