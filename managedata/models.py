from django.contrib.auth.models import User
from django.db import models

# Create your models here.



class CategoryBusiness(models.Model):
    description = models.CharField(max_length=240)


class Keyword(models.Model):
    keyword = models.CharField(max_length=50)
    category = models.ForeignKey('CategoryBusiness', on_delete=models.CASCADE, related_name='keywords')


class Business(models.Model):
    name = models.CharField(max_length=100)
    place_id = models.CharField(max_length=50)
    category = models.ForeignKey('CategoryBusiness', on_delete=models.CASCADE, related_name='related_business')


class Review(models.Model):
    author_id = models.CharField(max_length=50)
    complete_text = models.CharField(max_length=500)
    business = models.ForeignKey('Business', on_delete=models.CASCADE, related_name='reviews')


class Opinion(models.Model):
    text_pt = models.CharField(max_length=500)
    text_en = models.CharField(max_length=500)
    polality = models.IntegerField()
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='opinions')


class topic(models.Model):
    topic = models.CharField(max_length=240)
    opinion = models.ForeignKey('Opinion', on_delete=models.CASCADE, related_name='topics')
    relations_topics = models.ManyToManyField('self')


class BusinessPlan(models.Model):

    description = models.CharField(max_length=240)
    location = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class LateBusinessPlan(BusinessPlan):
    business = models.OneToOneField('Business', on_delete=models.CASCADE, related_name='late_business_plan')


class EarlyBusinessPlan(BusinessPlan):
    category = models.ForeignKey('CategoryBusiness', on_delete=models.CASCADE, related_name='early_business_plans')




