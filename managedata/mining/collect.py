from managedata.models import Keyword, Business, Review
import googlemaps as g

class CollectRival(object):

    def __init__(self, earlyBusinessPlan):
        self.category = earlyBusinessPlan.category
        self.keywords = Keyword.objects.filter(category=self.category)
        self.address = earlyBusinessPlan.location
        self.client = g.Client('AIzaSyB0UBbtTXcMS8DrdviSLxab9Oa0B_Dcclg')
        self.location = self.client.geocode(self.address)[0]['geometry']['location']


    def add_ids(self, result):
        places_ids = list(map(lambda x: x.place_id, Business.objects.filter(category=self.category)))
        for place in result:
            if place['place_id'] not in places_ids:
                Business.objects.create(name=place['name'], place_id=place['place_id'], category=self.category)


    def placesAll(self):
        placesList = []
        for query in self.keywords:
            result = self.client.places(query, self.location)
            self.add_ids(result['results'])
            while 'next_page_token' in result:
                try:
                    next = result['next_page_token']
                    result = self.client.places(query, self.location, page_token=next)
                    self.add_ids(result['results'])
                except:
                    continue
        return placesList


class CollectReview(object):

    def __init__(self, earlyBusinessPlan):
        self.category = earlyBusinessPlan.category
        self.client = g.Client('AIzaSyB0UBbtTXcMS8DrdviSLxab9Oa0B_Dcclg')


    def reviewAll(self):
        places_ids = list(map(lambda x: x.place_id, Business.objects.filter(category=self.category)))
        for id in places_ids:
            result = g.places.place(self.client, id, language=None)['result']
            business = Business.objects.get(place_id=id)
            for review in result.setdefault('reviews', {}):
                author_id = review['author_url'].split('/')[5]
                Review.objects.create(author_id=author_id, complete_text=review['text'], business=business)



