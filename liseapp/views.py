from audioop import reverse

from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views.defaults import page_not_found

from liseapp.forms import RegisterForm, NewPlanForm, RequestCategoryForm, EditDescriptionPlan, EditMyAccount
from liseapp.models import list_details_topics, list_weekdays, list_locations, Notification, list_weekhours_majority, \
    list_weekhours_minority, ranking_business
from managedata.models import Enterprising, BusinessPlan, Business, Review, Opinion, Topic, Branch, \
    CategoryBusiness, RequestCategory


def profileLoggedIn(request):
    return Enterprising.objects.get(user=request.user)

def dict_base(request):
    profile = profileLoggedIn(request)
    n = Notification.objects.filter(user=profile)[:5]
    n_not_viewed = Notification.objects.filter(user=profile, viewed=False)[:5]
    return {'notifications':n, 'noti_no_viewed': n_not_viewed}


def index(request):
    profile = profileLoggedIn(request)
    plans = BusinessPlan.objects.filter(enterprising=profile, status='ativo')
    if request.method == 'POST':
        form = EditDescriptionPlan(request.POST)
        if form.is_valid():
            plan = BusinessPlan.objects.get(id=form.cleaned_data.get('id'))
            plan.description = form.cleaned_data.get('description')
            plan.save(force_update=True)
            return redirect('liseapp:index')
    else:
        form = EditDescriptionPlan()
    vals = dict(dict_base(request), **{'plans':plans, 'form':form})
    return render(request, 'index.html', vals)


def myAccountDetails(request):
    profile = profileLoggedIn(request)

    if request.method == 'POST':
        form = EditMyAccount(request.POST)
        if form.is_valid():
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.save(force_update=True)
            profile.phone = form.cleaned_data.get('phone')
            profile.save(force_update=True)
            return redirect('liseapp:my-account-details')
    else:
        form = EditMyAccount()

    vals = dict(dict_base(request), **{'profile':profile, 'form':form})
    return render(request, 'my-account.html', vals)


def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('liseapp:my-account-details')
        else:
            messages.error(request, 'Please correct the error below.')
            print(form.errors)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change-password.html', {'form':form})


def forgotPassword(request):
    return render(request, 'forgot-password.html')


def dashboardDetails(request, plan_id):
    plan = BusinessPlan.objects.get(id=plan_id)
    rivals = Business.objects.filter(category=plan.category)
    reviews = Review.objects.filter(business__category=plan.category)
    topics = list_details_topics(category=plan.category)
    counts = list(map(lambda x: x['count'], topics))
    pos = list(map(lambda x: x['count_pos'], topics))
    neg = list(map(lambda x: x['count_neg'], topics))
    neu = list(map(lambda x: x['count_neu'], topics))
    nouns = list(map(lambda x: x['topic'].topic, topics))
    week_count = list_weekdays(category=plan.category)
    lng_lat = list_locations(category=plan.category)
    lng = list(map(lambda l: l[0], lng_lat))
    lat = list(map(lambda l: l[1], lng_lat))
    weekhours_max = list_weekhours_majority(category=plan.category)
    class_css = ['bg-pink', "bg-cyan", "bg-orange", "bg-teal", "bg-purple", 'bg-blue-grey', 'bg-indigo']
    for i, week in enumerate(weekhours_max): week.update({'class_css': class_css[i]})
    ranking = ranking_business(plan.category)[0:7]
    vals = dict(dict_base(request), **{'item':'all',
        'plan':plan, 'rivals': rivals, 'reviews': reviews, 'nouns':nouns, 'lngs': lng, 'lats': lat,
        'topics_count':counts, 'count_pos': pos, 'count_neg': neg, 'count_neu': neu, 'week_count': week_count,
        'weekhours_max':weekhours_max, 'ranking':ranking})
    return render(request, 'dashboard.html', vals)


def topTopics(request, plan_id):
    plan = BusinessPlan.objects.get(id=plan_id)
    topics = Topic.objects.filter(opinion__review__business__category=plan.category).distinct()
    topics_list = list_details_topics(category=plan.category)
    counts = list(map(lambda x: x['count'], topics_list))
    nouns = list(map(lambda x: x['topic'].topic, topics_list))
    vals = dict(dict_base(request), **{'item':'topics', 'subitem':'toptopics', 'plan':plan,
        'topics': topics, 'nouns':nouns, 'counts':counts})
    return render(request, 'top-topics.html', vals)


def polarityTopics(request, plan_id):
    plan = BusinessPlan.objects.get(id=plan_id)
    topics = list_details_topics(category=plan.category)
    counts = list(map(lambda x: x['count'], topics))
    pos = list(map(lambda x: x['count_pos'], topics))
    neg = list(map(lambda x: x['count_neg'], topics))
    neu = list(map(lambda x: x['count_neu'], topics))
    nouns = list(map(lambda x: x['topic'].topic, topics))
    vals = dict(dict_base(request), **{
        'plan':plan, 'topics':topics, 'nouns':nouns, 'item':'topics', 'subitem':'polaritytopics',
        'topics_count':counts, 'count_pos': pos, 'count_neg': neg, 'count_neu': neu})
    return render(request, 'polarity-topics.html', vals)


def rankingBusiness(request, plan_id):
    plan = BusinessPlan.objects.get(id=plan_id)
    ranking = ranking_business(plan.category)
    vals = dict(dict_base(request), **{'item':'business', 'subitem':'rankingbusiness', 'plan':plan, 'ranking':ranking})
    return render(request, 'ranking-business.html', vals)


def operatingDays(request, plan_id):
    plan = BusinessPlan.objects.get(id=plan_id)
    week_count = list_weekdays(category=plan.category)
    counts = list(map(lambda x: x[1], week_count))
    vals = dict(dict_base(request), **{'plan':plan,
        'item':'operating', 'subitem':'operatingdays', 'week_count':week_count, 'counts':counts})
    return render(request, 'operating-days.html', vals)


def operatingHours(request, plan_id):
    plan = BusinessPlan.objects.get(id=plan_id)
    weekhours_max = list_weekhours_majority(category=plan.category)
    weekhours_min = list_weekhours_minority(category=plan.category)
    class_css = ['bg-pink',"bg-cyan","bg-orange","bg-teal", "bg-purple",'bg-blue-grey','bg-indigo']
    for i, week in enumerate(weekhours_max): week.update({'class_css': class_css[i]})
    for i, week in enumerate(weekhours_min): week.update({'class_css': class_css[i]})
    vals = dict(dict_base(request), **{'item':'operating', 'subitem':'operatinghours', 'plan':plan,
                                       'weekhours_max':weekhours_max, 'weekhours_min':weekhours_min})
    return render(request, 'operating-hours.html', vals)


def competitionRegions(request, plan_id):
    plan = BusinessPlan.objects.get(id=plan_id)
    lng_lat = list_locations(category=plan.category)
    lng = list(map(lambda l: l[0], lng_lat))
    lat = list(map(lambda l: l[1], lng_lat))
    vals = dict(dict_base(request), **{
        'plan':plan, 'item':'maps', 'subitem':'competitionregions', 'lngs':lng, 'lats':lat})
    return render(request, 'competition-regions.html', vals)


def registerPlan(request):
    enterprising = profileLoggedIn(request)
    branchs = sorted(CategoryBusiness.objects.filter(active=True).values_list('branch__name', flat=True).distinct())
    categories = [(branch, sorted(CategoryBusiness.objects.filter(active=True, branch__name=branch)
                                .values_list('specialty', flat=True))) for branch in branchs]

    if 'form_register_plan' in request.POST:
        form1 = NewPlanForm(request.POST)
        if form1.is_valid():
            data = form1.cleaned_data
            branch = Branch.objects.get_or_create(name=data.get('branch'))[0]
            category = CategoryBusiness.objects.get(branch=branch, specialty=data.get('specialty'))
            plan = BusinessPlan.objects.create(description=data.get('description'),
                                                    state=data.get('state'),
                                                    city=data.get('city'),
                                                    enterprising=enterprising,
                                                    category=category,
                                                    create_date=date.today())
            Notification.objects.create(title='Novo plano de negócio criado',
                                        message='Seu plano cadastrado passará por uma primeira análise, em breve você '
                                                'poderá monitorá as informações dos seus possiveis concorrentes.',
                                        user=enterprising)
            return redirect('liseapp:index')
        print(form1.errors)
    else:
        form1 = NewPlanForm()
    if 'form_request_category' in request.POST:
        form2 = RequestCategoryForm(request.POST)
        if form2.is_valid():
            data = form2.cleaned_data
            RequestCategory.objects.create(enterprising=enterprising, specialty=data.get('specialty'),
                                           branch=data.get('branch'), description=data.get('description'))
            Notification.objects.create(title='Nova solicitação de categoria',
                                        message='A solicitação de categoria %s irá ser avaliada e em breve você '
                                                'receberá uma resposta.' % (form2.cleaned_data.get('specialty', '')),
                                        user=enterprising)
            return redirect('liseapp:index')
        print(form2.errors)
    else:
        form2 = RequestCategoryForm()

    vals = dict(dict_base(request), **{'branchs':branchs, 'categories':categories, 'form1':form1, 'form2':form2})

    return render(request, 'register-plan.html', vals)


def deletePlan(request, plan_id):
    plan = BusinessPlan.objects.get(id=plan_id)
    plan.status='cancelada'
    plan.save(force_update='True')
    Notification.objects.create(title='Análise de concorrentes cancelado',
                                message='Você cancelou o plano de negocio %d e não poderá mais análisar as informações.' % (plan.category.specialty),
                                user=profileLoggedIn(request))
    return redirect('liseapp:index')


def editPlan(request, plan_id):
    plan = BusinessPlan.objects.get(id=plan_id)
    branchs = CategoryBusiness.objects.filter(active=True).values_list('branch__name', flat=True).distinct()
    categories = [(branch, list(CategoryBusiness.objects.filter(active=True, branch__name=branch)
                                .values_list('specialty', flat=True))) for branch in branchs]
    vals = dict(dict_base(request), **{'plan': plan, 'categories':categories})
    return render(request, 'edit-plan.html', vals)


def pageNotifications(request, pk=False):
    noti = Notification.objects.get(id=pk) if pk else False
    if noti:
        noti.viewed = True
        noti.save(force_update=True)
    profile = profileLoggedIn(request)
    n = Notification.objects.filter(user=profile)
    vals = dict(dict_base(request), **{'notifications':n, 'select':noti})
    return render(request, 'notification.html', vals)


def signIn(request):
    return render(request, 'sign-in.html')


def signUp(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = form.cleaned_data.get('email')
            user.save(force_update=True)
            enter = Enterprising.objects.create(user=user, phone=form.cleaned_data.get('phone'))
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('liseapp:index')
        print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'sign-up.html', {'form': form})


def logout(request):
    return redirect('liseapp:signin')


def error404(request):
    return page_not_found(request, 'error-404.html')

