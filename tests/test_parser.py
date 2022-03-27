import unittest
from datetime import datetime

from app.models import LedgerEntity, EntityType
from app.parser import _csv_lines_to_dicts, csv_to_ledger_entities, _sanitize_csv_dicts


class TestCsvLinesToDicts(unittest.TestCase):
    def test_return_dicts(self):
        lines = [
           '"key1","key2","key3"',
           '"value1","value2","value3"',
           "value4,value5,value6",
        ]

        expected = [
            {
                '"key1"': '"value1"',
                '"key2"': '"value2"',
                '"key3"': '"value3"',
            },
            {
                '"key1"': 'value4',
                '"key2"': 'value5',
                '"key3"': 'value6',
            }
        ]

        self.assertEqual(expected, _csv_lines_to_dicts(lines))


class TestSanitizeCsvDicts(unittest.TestCase):
    def test_quotes_removed(self):
        dicts_with_quotes = [
            {
                '"key1"': '"value1"',
                '"key2"': '"value2"',
                '"key3"': '"value3"',
            },
            {
                '"key1"': 'value4',
                '"key2"': 'value5',
                '"key3"': 'value6',
            }
        ]

        expected = [
            {
                'key1': 'value1',
                'key2': 'value2',
                'key3': 'value3',
            },
            {
                'key1': 'value4',
                'key2': 'value5',
                'key3': 'value6',
            }
        ]

        self.assertEqual(_sanitize_csv_dicts(dicts_with_quotes), expected)

    def test_set_balance_to_zero_if_empty_string(self):
        dicts_with_balance = [{'balance': ''}]
        expected = [{"balance": 0}]
        self.assertEqual(_sanitize_csv_dicts(dicts_with_balance), expected)


class TestCsvToLedgerEntities(unittest.TestCase):
    def test_return_ledger_entities(self):
        csv = [
            '"txid","refid","time","type","subtype","aclass","asset","amount","fee","balance"',
            '"","QYTSNVJ-ZD76FK-VECNFC","2021-08-10 19:11:39","deposit","","currency","ZEUR",250.0000,9.6300,""',
            '"LU6M2Y-SW73C-7VIQMS","QYTSNVJ-ZD76FK-VECNFC","2021-08-10 19:12:40","deposit","","currency","EUR.HOLD",250.0000,9.6300,240.3700'
        ]

        ledger_entities = csv_to_ledger_entities(csv)

        assert len(ledger_entities) == 2

        entity0 = ledger_entities[0]
        assert "" == entity0.txid
        assert "QYTSNVJ-ZD76FK-VECNFC" == entity0.refid
        assert datetime(2021, 8, 10, 19, 11, 39) == entity0.time
        assert EntityType.DEPOSIT == entity0.entity_type
        assert "" == entity0.subtype
        assert "currency" == entity0.aclass
        assert "ZEUR" == entity0.asset
        assert 250.0 == entity0.amount
        assert 9.63 == entity0.fee
        assert 0.0 == entity0.balance

        entity1 = ledger_entities[1]
        assert "LU6M2Y-SW73C-7VIQMS" == entity1.txid
        assert "QYTSNVJ-ZD76FK-VECNFC" == entity1.refid
        assert datetime(2021, 8, 10, 19, 12, 40) == entity1.time
        assert EntityType.DEPOSIT == entity1.entity_type
        assert "" == entity1.subtype
        assert "EUR.HOLD" == entity1.asset
        assert 250.0 == entity1.amount
        assert 9.63 == entity1.fee
        assert 240.37 == entity1.balance
