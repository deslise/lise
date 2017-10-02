from managedata.mining.collect import CollectRival, CollectReview
from managedata.mining.summarization import Summarization
from managedata.models import *


def update_business_plan():
    plans = EarlyBusinessPlan.objects.all()
    for plan in plans:
        collect = CollectRival(plan)
        collect.placesAll()
        collect = CollectReview(plan)
        collect.reviewAll()
        summarize = Summarization(plan)
        summarize.identify_all_opinion_topics()


# update_business_plan()