from datetime import date, datetime

import facebook
from dateutil.relativedelta import relativedelta

from managedata.mining.classification import AnalyzeVader
from managedata.mining.organization import Organization
from managedata.models import Keyword, Business, Review, Opinion, Weekday
import googlemaps as g

class CollectRival(object):

    def __init__(self, businessPlan):
        self.category = businessPlan.category
        self.keywords = Keyword.objects.filter(category=self.category)
        self.address = businessPlan.location()
        self.client = g.Client('AIzaSyB0UBbtTXcMS8DrdviSLxab9Oa0B_Dcclg')
        self.location = self.client.geocode(self.address)[0]['geometry']['location']


    def add_ids(self, results):
        for result in results:
            place = g.places.place(self.client, result['place_id'], language=None)['result']
            sl= list(map(lambda x: x['short_name'],
                        filter(lambda x: 'sublocality' in x['types'], place.get('address_components',[]))))
            defaults={'name':place['name'],'category':self.category,'location':place['geometry']['location'],
                      'rating':place.get('rating',0),'sublocation':sl[0] if sl else '',
                      'phone':self.search_phone(place), 'website':self.search_website(place),
                      'facebook':self.search_id_facebook(place)}
            business = Business.objects.update_or_create(place_id=place['place_id'],defaults=defaults)
            self.collect_opening_hours(place, business[0])


    def search_phone(self, place):
        return place.get('formatted_phone_number', '')


    def search_website(self, place):
        return place.get('website', '')


    def search_id_facebook(self, place):
        ACCESS_TOKEN = '259215647870773|EHgeXOfZRcNs7yBMnro7yKTXo_8'
        f = facebook.GraphAPI(ACCESS_TOKEN)
        page = f.request("search", {'q': place['name']+' '+self.address.split(', ')[0],'type': 'page', 'limit':1})['data']
        return page[0]['id'] if page else ''




    def collect_opening_hours(self, place, business):
        if 'opening_hours' in place:
            for item in place['opening_hours']['weekday_text']:
                items = item.split(': ')
                detaults={'hours':items[1]}
                weekday = Weekday.objects.update_or_create(weekday=items[0], business=business, defaults=detaults)


    def placesAll(self):
        placesList = []
        for query in self.keywords:
            result = self.client.places(query, self.location)
            locais = filter(self.isNear, result['results'])
            self.add_ids(locais)
            while 'next_page_token' in result:
                try:
                    next = result['next_page_token']
                    result = self.client.places(query, self.location, page_token=next)
                    locais = filter(self.isNear, result['results'])
                    self.add_ids(locais)
                except:
                    continue
        return placesList

    def isNear(self, local):
        coo = local['geometry']['location']
        return (abs(self.location['lat'] - coo['lat']) <= 0.3 and abs(self.location['lng'] - coo['lng']) <= 0.3)


class CollectReview(object):

    def __init__(self, businessPlan):
        self.category = businessPlan.category
        self.client = g.Client('AIzaSyB0UBbtTXcMS8DrdviSLxab9Oa0B_Dcclg')


    def reviewAll(self):
        places_ids = list(map(lambda x: x.place_id, Business.objects.filter(category=self.category)))
        reviews_ids = list(map(lambda x: x.review_id, Review.objects.filter(business__category=self.category)))
        for id in places_ids:
            result = g.places.place(self.client, id, language=None)['result']
            business = Business.objects.get(place_id=id)
            for review in result.setdefault('reviews', {}):
                review_id = review['author_url'].split('/')[5] + '/' + id if review.get('author_url') else False
                if review_id and review_id not in reviews_ids and review['text'] != '':
                    review = Review.objects.create(review_id=review_id, complete_text=review['text'], business=business,
                            date_posted=self.calcule_date_posted(review['time']), date_collect=datetime.now())
                    self.saveOpinions(review)



    def calcule_date_posted(self, seconds):
        return date(1970,1,1) + relativedelta(seconds=+seconds)


    def saveOpinions(self, review):
        org = Organization()
        sentences = org.separate_sentences(review.complete_text)
        pattern = org.pattern_regex('managedata/util/stopwords.txt')
        sentences_dict = org.generate_keywords(sentences, pattern)
        vader = AnalyzeVader()
        for sentence in sentences_dict.items():
            polarity = vader.polarity(sentence[0])
            tokens = org.tokens_cogroo(sentence[1])
            lemmatized = ' '.join(map(lambda x: x.lemma, tokens))
            nouns = ' - '.join(map(lambda x: x.lexeme, filter(lambda x: x.pos == 'n', tokens)))
            Opinion.objects.create(text_pt=sentence[1], text_en=sentence[0], polarity=polarity, review=review,
                                   lemmatized=lemmatized, nouns=nouns)






