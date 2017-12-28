from managedata.models import BusinessPlan, Enterprising


def permission_access_plan(request, plan):
    enter = Enterprising.objects.get(user=request.user)
    if plan.enterprising == enter:
        return True
    return False