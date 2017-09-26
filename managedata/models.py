from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Branch(models.Model):
    name = models.CharField(max_length=240)

    def __str__(self):
        return self.name



class CategoryBusiness(models.Model):
    specialty = models.CharField(max_length=240)
    branch = models.ForeignKey('Branch', related_name='categories')

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

    def __str__(self):
        return self.name


class Review(models.Model):
    author_id = models.CharField(max_length=50)
    complete_text = models.CharField(max_length=500)
    business = models.ForeignKey('Business', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.complete_text


class Opinion(models.Model):
    text_pt = models.CharField(max_length=500)
    text_en = models.CharField(max_length=500)
    polality = models.IntegerField()
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='opinions')

    def __str__(self):
        return self.text_pt


class Topic(models.Model):
    topic = models.CharField(max_length=240)
    opinion = models.ForeignKey('Opinion', on_delete=models.CASCADE, related_name='topics')
    relations_topics = models.ManyToManyField('self')

    def __str__(self):
        return self.topic


class BusinessPlan(models.Model):

    description = models.CharField(max_length=240)
    location = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class LateBusinessPlan(BusinessPlan):
    business = models.OneToOneField('Business', on_delete=models.CASCADE, related_name='late_business_plan')

    def __str__(self):
        return self.description + ' (late)'


class EarlyBusinessPlan(BusinessPlan):
    category = models.ForeignKey('CategoryBusiness', on_delete=models.CASCADE, related_name='early_business_plans')

    def __str__(self):
        return self.description + ' (early)'




