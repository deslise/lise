from cogroo_interface import Cogroo

from managedata.models import ItemTopic, Opinion


class Summarization(object):

    def __init__(self, plan):
        self.cogroo = Cogroo.Instance()
        self.plan = plan


    def identify_opinion_topics(self, opinion):
        try:
            nouns = map(lambda n: self.cogroo.analyze(n).sentences[0].tokens[0], opinion.nouns.split(' - '))
            topics = self.check_topics(nouns, opinion)
            for topic in topics:
                opinion.topics.add(topic)
        except Exception as e:
            print(e)


    def check_topics(self, nouns, opinion):
        category = opinion.review.business.category
        topics = []
        for noun in nouns:
            itemsTopics = ItemTopic.objects.filter(lemma=noun.lemma)
            if itemsTopics:
                item = itemsTopics.first()
                if category in item.categories.all():
                    if item.status == 'ativo': topics.append(itemsTopics[0].topic)
                else:
                    item.status = 'novo'
                    item.context = opinion.text_pt
                    item.save(force_update=True)
                    item.categories.add(category)
            else:
                item = ItemTopic.objects.create(lemma=noun.lemma,context=opinion.text_pt)
                item.categories.add(category)
                print(noun.lemma)
        return topics


    def identify_all_opinion_topics(self):
        opinions = Opinion.objects.filter(review__business__category=self.plan.category)
        for opinion in opinions:
            self.identify_opinion_topics(opinion)


