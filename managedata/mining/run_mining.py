from managedata.mining.collect import CollectRival
from managedata.models import *


def update_business_plan():
    plans = EarlyBusinessPlan.objects.all()
    for plan in plans:
        collect = CollectRival(plan)
        collect.placesAll()


# update_business_plan()