import json

from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db import models

# Create your models here.
from django.db.models import Count
from django.core.urlresolvers import reverse

from managedata.models import Opinion, Topic, Weekday, Business, Enterprising


class Notification(models.Model):
    title = models.CharField(max_length=248)
    message = models.TextField()
    date = models.DateField()
    user = models.ForeignKey(Enterprising, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']


    def __str__(self):
        return self.title


    def days_ago_created(self):
        ago = (date.today() - self.date).days
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



def list_locations(category):
    locations = list(map(lambda b: b.location.split(', '), Business.objects.filter(category=category)))
    lng_lat = []
    for l in locations:
        if 'lng' in l[0] and 'lat' in l[1]:
            lng_lat.append((l[0].split(': ')[1], l[1].split(': ')[1][:-1]))
        elif 'lat' in l[0] and 'lng' in l[1]:
            lng_lat.append((l[1].split(': ')[1][:-1], l[0].split(': ')[1]))
    return lng_lat


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




