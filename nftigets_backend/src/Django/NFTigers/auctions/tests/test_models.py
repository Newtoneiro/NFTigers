from django.test import TestCase

from auctions.models import NftCategory, SchoolClass


class NftCategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        NftCategory.objects.create(
            category_id=0,
            name="test"
        )

    def test_str(self):
        category = NftCategory.objects.get(category_id=0)
        self.assertEqual(str(category), 'test')


class SchoolClassModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SchoolClass.objects.create(
            schoolclass_id=0,
            name="A",
            start_year="2000"
        )

    def test_str(self):
        schoolclass = SchoolClass.objects.get(schoolclass_id=0)
        self.assertEqual(str(schoolclass), '2000 - A')
