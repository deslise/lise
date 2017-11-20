from datetime import date
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Enterprising(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.first_name



class Branch(models.Model):
    name = models.CharField(max_length=240)

    def __str__(self):
        return self.name


class RequestCategory(models.Model):
    specialty = models.CharField(max_length=240)
    branch = models.CharField(max_length=240)
    description = models.TextField()
    accept = models.BooleanField(default=True)


    def __str__(self):
        return self.specialty + ' - ' + self.branch



class CategoryBusiness(models.Model):
    specialty = models.CharField(max_length=240)
    branch = models.ForeignKey('Branch', related_name='categories')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.specialty


class Keyword(models.Model):
    keyword = models.CharField(max_length=50)
    category = models.ForeignKey('CategoryBusiness', on_delete=models.CASCADE, related_name='keywords')

    def __str__(self):
        return self.keyword


class Business(models.Model):
    name = models.CharField(max_length=100)
    place_id = models.CharField(max_length=50)
    category = models.ForeignKey('CategoryBusiness', on_delete=models.CASCADE, related_name='related_business')
    location = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Weekday(models.Model):
    weekday = models.CharField(max_length=20)
    hours = models.CharField(max_length=20)
    business = models.ForeignKey('Business', on_delete=models.CASCADE, related_name='weekdays')

    def __str__(self):
        return self.weekday + ' - ' + self.business.name


class Review(models.Model):
    review_id = models.CharField(max_length=50)
    complete_text = models.CharField(max_length=500)
    business = models.ForeignKey('Business', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.complete_text


class Topic(models.Model):
    topic = models.CharField(max_length=50)
    description = models.CharField(max_length=240)


    def __str__(self):
        return self.topic


class ItemTopic(models.Model):
    noun = models.CharField(max_length=50)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, related_name='itemtopics')
    categories = models.ManyToManyField('CategoryBusiness')


    def __str__(self):
        return self.noun


class Opinion(models.Model):
    text_pt = models.CharField(max_length=500)
    text_en = models.CharField(max_length=500)
    polarity = models.IntegerField()
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='opinions')
    topics = models.ManyToManyField('Topic', blank=True)

    def __str__(self):
        return self.text_pt


class BusinessPlan(models.Model):

    STATUS = (('solicitada','Solicitada'),('ativa','Ativa'),('cancelada','Cancelada'))
    description = models.CharField(max_length=240)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    enterprising = models.ForeignKey('Enterprising', on_delete=models.CASCADE)
    create_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS, default='solicitada')

    def ageDays(self):
        return (date.today() - self.create_date).days

    def location(self):
        return '%s, %s' % (self.city, self.state)

    class Meta:
        abstract = True


class LateBusinessPlan(BusinessPlan):
    business = models.OneToOneField('Business', on_delete=models.CASCADE, related_name='late_business_plan')

    def __str__(self):
        return self.business.name + ' (BusinessPlan)'


class EarlyBusinessPlan(BusinessPlan):
    category = models.ForeignKey('CategoryBusiness', on_delete=models.CASCADE, related_name='early_business_plans')

    def __str__(self):
        return self.category.specialty + ' (BusinessPlan)'





