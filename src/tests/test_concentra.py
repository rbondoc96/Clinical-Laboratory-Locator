from unittest import TestCase

from navs.concentra import ConcentraSearch

class TestConcentra(TestCase):

    def test_search(self):
        zipcode = 92108
        search = ConcentraSearch(zipcode)
        limit = 100

        result = search.search(limit=limit)
        self.assertTrue(len(result) > 0 and len(result) <= limit)

        search.set_params(
            zipcode=57001
        )
        result = search.search()
        self.assertTrue(len(result) == 0)

        with self.assertRaises(ValueError):
            search.set_params(zipcode=None)
