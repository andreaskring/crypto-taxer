import unittest

from parameterized import parameterized

from app.parser import _csv_lines_to_dicts


class TestCsvLinesToDicts(unittest.TestCase):

    @parameterized.expand(
        [
            (
                [
                    "key1,key2,key3",
                    "value1,value2,value3",
                    "value4,value5,value6",
                ],
            ),
            (
                [
                    '"key1","key2","key3"',
                    '"value1","value2","value3"',
                    "value4,value5,value6",
                ],
            )
        ]
    )
    def test_return_dicts(self, lines):
        expected = [
            {
                "key1": "value1",
                "key2": "value2",
                "key3": "value3",
            },
            {
                "key1": "value4",
                "key2": "value5",
                "key3": "value6",
            }
        ]

        self.assertEqual(expected, _csv_lines_to_dicts(lines))
