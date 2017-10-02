import unittest

from django.test import TestCase

# Create your tests here.
from managedata.mining.classification import AnalyzeVader
from managedata.mining.collect import CollectRival, CollectReview
from managedata.mining.organization import Organization
from managedata.models import EarlyBusinessPlan, Business, Review, Opinion
import managedata.mining.run_mining as run


class TestCollectRival(TestCase):
    """docstring for TesteCollectRival"""

    fixtures = ['text_fixtures.json']

    def setUp(self):
        self.plan = EarlyBusinessPlan.objects.get(id=1)
        self.collect = CollectRival(earlyBusinessPlan=self.plan)

    @unittest.skip('não precisa ser testado agora')
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

    @unittest.skip('não precisa ser testado agora')
    def test_reviews_all(self):
        self.collect.reviewAll()
        reviews_all = Review.objects.filter(business__category=self.plan.category)
        opinions_all = Opinion.objects.filter(review__business__category=self.plan.category)
        print('Reviews All: %d' % len(reviews_all))
        print('Opinion All: %d' % len(opinions_all))


class TestOrganization(TestCase):

    fixtures = ['text_fixtures.json']

    def setUp(self):
        self.plan = EarlyBusinessPlan.objects.get(id=1)
        self.reviews = Review.objects.filter(business__category=self.plan.category)
        self.org = Organization()

    @unittest.skip('não precisa ser testado agora')
    def test_all_separete_senteces(self):
        allSentences = self.org.all_separate_sentences(self.reviews)
        print('Todas sentenças: %d' % len(allSentences))
        print(allSentences)

    @unittest.skip('não precisa ser testado agora')
    def test_clean_sentence(self):
        sentence =  "O sabor quase que inigualável"
        pattern_regex = self.org.pattern_regex('managedata/util/stopwords.txt')
        clean_sentence = self.org.clean_sentence(sentence, pattern_regex)
        self.assertEqual('Sabor quase inigualável', clean_sentence)

    @unittest.skip('não precisa ser testado agora')
    def test_validate_sentece_true(self):
        sentence = 'Sabor quase inigualável'
        self.assertTrue(self.org.validate_sentence(sentence), 'A sentença foi não validada corretamente')

    @unittest.skip('não precisa ser testado agora')
    def test_validate_sentece_false(self):
        sentence = 'Muito saborosas'
        self.assertFalse(self.org.validate_sentence(sentence), 'A sentença foi não validada corretamente')

    @unittest.skip('não precisa ser testado agora')
    def test_generate_keywords(self):
        allSentences = self.org.all_separate_sentences(self.reviews)
        pattern_regex = self.org.pattern_regex('managedata/util/stopwords.txt')
        keywords = self.org.generate_keywords(allSentences, pattern_regex)
        print('Keywords: %d' % len(keywords))
        print(keywords)


class TestAnalyzeVader(TestCase):

    fixtures = ['text_fixtures.json']

    def setUp(self):
        self.vader = AnalyzeVader()

    @unittest.skip('não precisa ser testado agora')
    def test_polarity_pos(self):
        phrase = 'Pretty good and cheap'
        self.assertEqual(1, self.vader.polarity(phrase), 'Polaridade errada')

    @unittest.skip('não precisa ser testado agora')
    def test_polarity_neg(self):
        phrase = 'And poor service'
        self.assertEqual(-1, self.vader.polarity(phrase), 'Polaridade errada')


class TestRunMining(TestCase):

    fixtures = ['text_fixtures.json']

    def test_update(self):
        run.update_business_plan()

