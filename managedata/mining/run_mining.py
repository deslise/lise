from datetime import datetime

from managedata.mining.collect import CollectRival, CollectReview
from managedata.mining.summarization import Summarization
from managedata.models import *


def update_business_plan():
    start = datetime.now()
    plans = BusinessPlan.objects.exclude(status='cancelado')
    for plan in plans:
        collect = CollectRival(plan)
        collect.placesAll()
        collect = CollectReview(plan)
        collect.reviewAll()
        summarize = Summarization(plan)
        summarize.identify_all_opinion_topics()
        plan.status = 'ativo'
        plan.save()
    end = datetime.now()
    numero = max(list(map(lambda up: up.numero, DataUpdate.objects.all())) or [0])+1
    date_update = DataUpdate.objects.create(datetime_start=start,
                                            datetime_end=end,
                                            numero=numero)
    for plan in plans: date_update.plans.add(plan)
    return True
    



# update_business_plan()