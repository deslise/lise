from managedata.mining.collect import CollectRival, CollectReview
from managedata.models import *


def update_business_plan():
    plans = EarlyBusinessPlan.objects.all()
    for plan in plans:
        collect = CollectRival(plan)
        collect.placesAll()
        collect = CollectReview(plan)
        collect.reviewAll()


# update_business_plan()