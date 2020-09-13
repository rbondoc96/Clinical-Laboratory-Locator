from unittest import TestCase

from navs.labcorp import LabcorpSearch

class TestLabcorp(TestCase):

    def test_search(self):

        # Area with locations
        zipcode = 92108
        radius = 25
        service = LabcorpSearch.BLOODWORK
        search = LabcorpSearch(
            zipcode,
            radius=radius,
            service=service
        )
        limit = 100

        result = search.search(limit=limit)
        self.assertTrue(len(result) > 0 and len(result) <= limit)

        # Remote area with no locations
        search.set_params(
            zipcode=57001,
            radius=100,
            service=LabcorpSearch.DRUG_SCREEN_COLLECTION
        )
        result = search.search(limit=50)
        print(result)
        self.assertTrue(len(result) == 0)

        

        