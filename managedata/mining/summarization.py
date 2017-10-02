from cogroo_interface import Cogroo

from managedata.models import ItemTopic, Opinion


class Summarization(object):

    def __init__(self, plan):
        self.cogroo = Cogroo.Instance()
        self.plan = plan


    def identify_opinion_topics(self, opinion):
        try:
            nouns = list(filter(lambda x: x.pos == 'n', self.cogroo.analyze(opinion.text_pt.lower()).sentences[0].tokens))
            topics = self.check_topics(nouns, opinion.review.business.category)
            for topic in topics:
                if not topic in opinion.topics.get_queryset():
                    opinion.topics.add(topic)
        except Exception as e:
            print(e)

    def check_topics(self, nouns, category):
        topics = []
        for noun in nouns:
            itemsTopics = ItemTopic.objects.filter(categories=category, noun=noun.lemma)
            if itemsTopics:
                topics.append(itemsTopics[0].topic)
            else:
                print(noun.lemma)
        return topics


    def identify_all_opinion_topics(self):
        opinions = Opinion.objects.filter(review__business__category=self.plan.category)
        for opinion in opinions:
            self.identify_opinion_topics(opinion)

