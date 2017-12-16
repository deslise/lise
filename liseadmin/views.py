from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from liseadmin.forms import RefuseRequests, AcceptRequests
from liseapp.models import Notification
from managedata.mining.run_mining import update_business_plan
from managedata.models import RequestCategory, CategoryBusiness, DataUpdate, Topic, ItemTopic, BusinessPlan, \
    Enterprising


def requestCategories(request):
    requests = RequestCategory.objects.filter(status='pendente')
    historic = RequestCategory.objects.exclude(status='pendente')
    vals = {'requests':requests, 'historic':historic}
    return render(request, 'request-categories.html', vals)


def manageCategories(request):
    categories = CategoryBusiness.objects.all()
    vals = {'categories':categories}
    return render(request, 'manage-categories.html', vals)


def acceptRequest(request, req_id):
    req = RequestCategory.objects.get(id=req_id)
    if request.method == 'POST':
        form = AcceptRequests(request.POST)
        if form.is_valid():
            category = form.cleaned_data.get('category_related')
            req.category_related = category
            req.status = 'aceito'
            req.save(force_update=True)
            Notification.objects.create(title='Solicitação de categoria aceita',
                                        message='A solicitação de categoria %s foi aceita.\nA categoria desejada é a %s do ramo %s' % (
                                        req.specialty, category.specialty, category.branch.first().name),
                                        user=req.enterprising)
            return redirect('liseadmin:request-categories')
        print(form.errors)
    else:
        form = AcceptRequests()
    vals = {'form': form, 'req_id': req_id}
    return render(request, 'accept-request.html', vals)


def refuseRequest(request, req_id):
    req = RequestCategory.objects.get(id=req_id)
    if request.method == 'POST':
        form = RefuseRequests(request.POST)
        if form.is_valid():
            reason = form.cleaned_data.get('reason')
            req.reason_refuse = reason
            req.status = 'recusado'
            req.save(force_update=True)
            Notification.objects.create(title='Solicitação de categoria recusada',
                                        message='A solicitação de categoria %s foi recusada.\nMotivo: %s' % (req.specialty, reason),
                                        user=req.enterprising)
            return redirect('liseadmin:request-categories')
        print(form.errors)
    else:
        form = RefuseRequests()
    vals = {'form':form,'req_id':req_id}
    return render(request, 'refuse-request.html', vals)




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
        items.extend(map(lambda i: {'noun':i.lemma, 'topic':i.topic, 'category':c},it))
    vals = {'topics':topics,'items':items}
    return render(request, 'manage-topics.html', vals)