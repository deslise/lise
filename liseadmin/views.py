from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from managedata.mining.run_mining import update_business_plan
from managedata.models import RequestCategory, CategoryBusiness, DataUpdate, Topic, ItemTopic, BusinessPlan


def requestCategories(request):
    requests = RequestCategory.objects.filter(status='pendente')
    historic = RequestCategory.objects.exclude(status='pendente')
    vals = {'requests':requests, 'historic':historic}
    return render(request, 'request-categories.html', vals)


def manageCategories(request):
    categories = CategoryBusiness.objects.all()
    vals = {'categories':categories}
    return render(request, 'manage-categories.html', vals)


def setStateRequest(request, req_id, state):
    req = RequestCategory.objects.get(id=req_id)
    req.set_status(state)
    return redirect('liseadmin:request-categories')


def managePlan(request):
    plans = BusinessPlan.objects.all()
    vals = {'plans':plans}
    return render(request, 'manage-plan.html', vals)


def manageData(request):
    updates = DataUpdate.objects.all()
    vals = {'updates':updates}
    return render(request, 'manage-data.html', vals)

def updateData(request):
    update = update_business_plan()
    return JsonResponse({'update':update})

def recusarItem(request, item_id):
    item = ItemTopic.objects.get(id=item_id)
    item.status = 'recusado'
    item.save()
    return JsonResponse({})

def newItems(request):
    items = ItemTopic.objects.filter(status='novo')
    vals = {'items':items}
    return render(request, 'new-items.html', vals)




def manageTopics(request):
    topics = Topic.objects.all()
    items = []
    for c in CategoryBusiness.objects.all():
        it = ItemTopic.objects.filter(categories=c,status='ativo')
        items.extend(map(lambda i: {'noun':i.noun, 'topic':i.topic, 'category':c},it))
    vals = {'topics':topics,'items':items}
    return render(request, 'manage-topics.html', vals)