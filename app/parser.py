from copy import deepcopy

from more_itertools import unique_everseen
from typing import List, Dict, Any, Tuple

from app.models import LedgerEntity


EURO_KEYS = ("ZEUR", "EUR.HOLD")


def _csv_lines_to_dicts(csv: List[str]) -> List[Dict[str, Any]]:
    keys = csv[0].split(",")
    # assert keys == [
    #     "txid", "refid", "time", "subtype", "aclass", "asset", "amount", "fee", "balance"
    # ]
    values = map(lambda line: line.split(","), csv[1:])
    dicts = [dict(zip(keys, value)) for value in values]
    return dicts


def _sanitize_csv_dicts(dicts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    def remove_quotes(s: str) -> str:
        return s.replace('"', '')

    def fix_empty_balance(d: Dict[str, Any]) -> Dict[str, Any]:
        sanitized_dict = deepcopy(d)
        if sanitized_dict.get("balance") == '':
            sanitized_dict["balance"] = None
        return sanitized_dict

    # Remove quotes from keys and values in dicts
    sanitized_dicts = [
        {
            remove_quotes(key): remove_quotes(value)
            for key, value in d.items()
        }
        for d in dicts
    ]

    # Sanitize balance field
    sanitized_dicts = map(fix_empty_balance, sanitized_dicts)

    return list(sanitized_dicts)


def csv_to_ledger_entities(csv: List[str]) -> List[LedgerEntity]:
    dicts = _csv_lines_to_dicts(csv)
    dicts = _sanitize_csv_dicts(dicts)
    ledger_entities = map(lambda d: LedgerEntity.parse_obj(d), dicts)
    return list(ledger_entities)


def get_asset_types(entities: List[LedgerEntity]) -> Tuple[str]:
    assets = map(lambda entity: entity.asset, entities)
    assets = unique_everseen(assets)
    assets = filter(lambda asset: asset not in EURO_KEYS, assets)
    return tuple(assets)
