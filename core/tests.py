from django.test import TestCase
from core.utils.utils import concatenateLists, getDisctionaryOfLists


class ArrayOfDictionariesToDictionatyOfArraysTest(TestCase):
    def setUp(self):
        self.myInput = [
            {"input_month": 1, "input_year": 2021, "count": 1},
            {"input_month": 2, "input_year": 2021, "count": 2},
            {"input_month": 1, "input_year": 2022, "count": 5},
            {"input_month": 2, "input_year": 2022, "count": 4},
            {"input_month": 3, "input_year": 2022, "count": 3},
            {"input_month": 4, "input_year": 2022, "count": 2},
            {"input_month": 5, "input_year": 2022, "count": 1},
        ]

    def test_getDisctionaryOfLists_function(self):
        dict = getDisctionaryOfLists(self.myInput)
        self.assertEqual(dict["input_month"], [1, 2, 1, 2, 3, 4, 5])
        self.assertEqual(dict["input_year"], [2021, 2021, 2022, 2022, 2022, 2022, 2022])
        self.assertEqual(dict["count"], [1, 2, 5, 4, 3, 2, 1])


class ConcatenateListsTest(TestCase):
    def setUp(self):
        self.years = [2020, 2020, 2021, 2021, 2021, 2022, 2022, 2022]
        self.months = [1, 2, 1, 2, 3, 1, 2, 3]

    def test_concatenate_lists(self):
        newList = concatenateLists(self.months, self.years, "-")
        self.assertEqual(
            newList,
            [
                "1-2020",
                "2-2020",
                "1-2021",
                "2-2021",
                "3-2021",
                "1-2022",
                "2-2022",
                "3-2022",
            ],
        )
