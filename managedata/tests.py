import unittest

from django.test import TestCase

# Create your tests here.
from managedata.mining.collect import CollectRival, CollectReview
from managedata.models import EarlyBusinessPlan, Business, Review


class TestCollectRival(TestCase):
    """docstring for TesteCollectRival"""

    fixtures = ['text_fixtures.json']

    def setUp(self):
        self.plan = EarlyBusinessPlan.objects.get(id=1)
        self.collect = CollectRival(earlyBusinessPlan=self.plan)

    # @unittest.skip('não precisa ser testado agora')
    def test_places_all(self):
        self.collect.placesAll()
        rivals_all = Business.objects.filter(category=self.plan.category)
        print('Rivals All: %d' % len(rivals_all))
        print(rivals_all)

class TestCollectReview(TestCase):

    fixtures = ['text_fixtures.json']

    def setUp(self):
        self.plan = EarlyBusinessPlan.objects.get(id=1)
        self.collect = CollectReview(earlyBusinessPlan=self.plan)


    def test_reviews_all(self):
        self.collect.reviewAll()
        reviews_all = Review.objects.filter(business__category=self.plan.category)
        print('Reviews All: %d' % len(reviews_all))
        print(reviews_all)