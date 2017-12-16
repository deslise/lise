import json

from datetime import date, datetime
from functools import reduce

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db import models
from django.utils import timezone

# Create your models here.
from django.db.models import Count
from django.core.urlresolvers import reverse

from managedata.models import Opinion, Topic, Weekday, Business, Enterprising


class Notification(models.Model):
    title = models.CharField(max_length=248)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(Enterprising, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']


    def __str__(self):
        return self.title


    def days_ago_created(self):
        ago = (timezone.now().date() - self.date.date()).days
        return 'hoje' if ago == 0 else '1 dia atrás'if ago==1 else '%d dias atrás' % (ago)

    def get_href(self):
        return reverse('liseapp:notifications', kwargs={'pk':self.id})



def list_details_topics(category):
    topics = Opinion.objects.filter(review__business__category=category) \
        .values('topics').exclude(topics=None) \
        .annotate(count=Count('topics')) \
        .distinct() \
        .order_by('-count')
    for topic in topics:
        topic['topic'] = Topic.objects.get(id=topic['topics'])
        topic['count_pos'] = Opinion.objects.filter(topics=topic['topics'],polarity=1).count()
        topic['count_neg'] = Opinion.objects.filter(topics=topic['topics'],polarity=-1).count()
        topic['count_neu'] = Opinion.objects.filter(topics=topic['topics'],polarity=0).count()

    return topics


def list_weekdays(category):
    weekday = Weekday.objects.filter(business__category=category).values('weekday').exclude(hours='Closed').annotate(
        count=Count('weekday'))
    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    semana = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
    l = []
    total = Weekday.objects.filter(business__category=category).count()/7
    for i in range(0,7):
        l.append((semana[i], '%.2f' % (weekday.filter(weekday=weekdays[i])[0]['count']/total * 100)))
    return l


def convert_hours(hour):
    open_close = ['–––', '–––']
    if hour == 'Open 24 hours':
        open_close = ['00:00','00:00']
    if '–' in hour:
        for i, str_h in enumerate(hour.split(' – ')):
            if 'AM' in str_h:
                open_close[i] = str_h.replace(' AM', '')
            elif 'PM' in str_h:
                h, m = str_h.replace(' PM', '').split(':')
                open_close[i] = str(int(h)+12)+':'+m
            else:
                open_close[i] = str_h
    return tuple(open_close)


def list_weekhours_majority(category):
    weekday = Weekday.objects.filter(business__category=category).values('weekday', 'hours').annotate(
        count=Count('weekday'))
    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    semana = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
    l = []
    for i in range(0,7):
        weekhour = list(filter(lambda x: x.get('weekday')==weekdays[i], weekday))
        max_hour = max(map(lambda x:x.get('count'), weekhour))
        hour = list(map(lambda x: x.get('hours'), filter(lambda x: x.get('count')==max_hour, weekhour)))[0]
        max_hour_open, max_hour_close = convert_hours(hour)
        l.append({'week':semana[i],'open':max_hour_open, 'close':max_hour_close})
    return l


def list_weekhours_minority(category):
    weekday = Weekday.objects.filter(business__category=category).values('weekday', 'hours').annotate(
        count=Count('weekday'))
    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    semana = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
    l = []
    for i in range(0,7):
        weekhour = list(filter(lambda x: x.get('weekday')==weekdays[i], weekday))
        min_hour = min(map(lambda x:x.get('count'), weekhour))
        hour = list(map(lambda x: x.get('hours'), filter(lambda x: x.get('count')==min_hour, weekhour)))[0]
        min_hour_open, min_hour_close = convert_hours(hour)
        l.append({'week':semana[i],'open':min_hour_open, 'close':min_hour_close})
    return l


def list_locations(category):
    locations = list(map(lambda b: b.location.split(', '), Business.objects.filter(category=category)))
    lng_lat = []
    for l in locations:
        if 'lng' in l[0] and 'lat' in l[1]:
            lng_lat.append((l[0].split(': ')[1], l[1].split(': ')[1][:-1]))
        elif 'lat' in l[0] and 'lng' in l[1]:
            lng_lat.append((l[1].split(': ')[1][:-1], l[0].split(': ')[1]))
    return lng_lat


def score_business(business):
    pos = Opinion.objects.filter(review__business=business, polarity=1).count()
    score = (pos * business.rating) or business.rating
    return score


def ranking_business(category):
    business = Business.objects.filter(category=category)
    l = [(b.name,score_business(b)) for b in business]
    ranking = []
    for i, b in enumerate(sorted(l, key=lambda x: x[1], reverse=True)):
        ranking.append({'position':i+1, 'name':b[0], 'score':round(b[1],2)})
    return ranking


def list_sublocations(category):
    business = Business.objects.filter(category=category).values('sublocation').exclude(sublocation='')
    total = business.count()
    b_by_l = business.annotate(count=Count('sublocation')).order_by('-count')
    sublocation, count = [], []
    for bl in b_by_l:
        sublocation.append(bl['sublocation'])
        count.append(round((bl['count']/total)*100, 2))
    return sublocation, count


def list_sublocations_small(category):
    sublocation, count = list_sublocations(category)
    sublocation = sublocation[:4]+['Outros']
    rest = reduce(lambda x,y: x+y, count[4:])
    total = reduce(lambda x,y:x+y, count)
    count = count[:4]+[round(rest/total*100,2)]
    return sublocation,count


def prepare_opinions(category):
    opinions_pos = Opinion.objects.filter(review__business__category=category, polarity=1)
    opinions_neg = Opinion.objects.filter(review__business__category=category, polarity=-1)
    pos, neg = black_noun_text(opinions_pos), black_noun_text(opinions_neg)
    # pos, neg = opinions_pos, opinions_neg
    return pos, neg


def black_noun_text(opinions):
    l = []
    for op in opinions:
        text = op.text_pt
        for noun in op.nouns.split(' - '):
            text = text.replace(noun.lower(), '<b>%s</b>' % noun).replace(noun.capitalize(), '<b>%s</b>' % noun.capitalize())
        l.append({'text_pt': text, 'review': op.review})
    return l


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None




