from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Enterprising(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.first_name


    def get_admin_url(self):
        return '/admin/managedata/enterprising/'+str(self.id)



class Branch(models.Model):
    name = models.CharField(max_length=240, unique=True)

    def __str__(self):
        return self.name


class RequestCategory(models.Model):
    STATUS = (('pendente','Pendente'),
              ('aceito','Aceito'),
              ('recusado','Recusado'))
    specialty = models.CharField(max_length=240)
    branch = models.CharField(max_length=240)
    description = models.TextField()
    status = models.CharField(max_length=8, choices=STATUS, default='pendente')
    date_request = models.DateTimeField(default=timezone.now())
    reason_refuse = models.TextField(null=True, blank=True)
    enterprising = models.ForeignKey('Enterprising', on_delete=models.CASCADE, related_name='requests')
    category_related = models.ForeignKey('CategoryBusiness', on_delete=models.CASCADE, related_name='requestcategories', blank=True, null=True)

    def __str__(self):
        return self.specialty + ' - ' + self.branch

    def set_status(self, choice):
        self.status = choice
        self.save(force_update=True)

    def get_admin_url(self):
        return '/admin/managedata/requestcategory/' + str(self.id)



class CategoryBusiness(models.Model):
    specialty = models.CharField(max_length=240, unique=True)
    branch = models.ManyToManyField('Branch')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.specialty


    def list_branchs(self):
        l = sorted(self.branch.all().values_list('name', flat=True))
        return ', '.join(l)

    def quantBusiness(self):
        return len(BusinessPlan.objects.filter(category=self))


    def get_admin_url(self):
        return '/admin/managedata/categorybusiness/' + str(self.id)

    def list_keywords(self):
        return Keyword.objects.filter(category=self)



class Keyword(models.Model):
    keyword = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey('CategoryBusiness', on_delete=models.CASCADE, related_name='keywords')


    class Meta:
        ordering = ['keyword']

    def __str__(self):
        return self.keyword

    def get_admin_url(self):
        return '/admin/managedata/keyword/'+str(self.id)


class Business(models.Model):
    name = models.CharField(max_length=100)
    place_id = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey('CategoryBusiness', on_delete=models.CASCADE, related_name='related_business')
    location = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    sublocation = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=50, default='', blank=True)
    website = models.CharField(max_length=50, default='', blank=True)
    facebook = models.CharField(max_length=30, default='', blank=True)


    def __str__(self):
        return self.name


class Weekday(models.Model):
    weekday = models.CharField(max_length=20)
    hours = models.CharField(max_length=20)
    business = models.ForeignKey('Business', on_delete=models.CASCADE, related_name='weekdays')

    def __str__(self):
        return self.weekday + ' - ' + self.business.name


class Review(models.Model):
    review_id = models.CharField(max_length=50, unique=True)
    complete_text = models.CharField(max_length=500)
    business = models.ForeignKey('Business', on_delete=models.CASCADE, related_name='reviews')
    date_posted = models.DateTimeField(blank=True, null=True)
    date_collect = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.complete_text


class Topic(models.Model):
    topic = models.CharField(max_length=50)
    description = models.CharField(max_length=240)


    def __str__(self):
        return self.topic


    def numberItems(self):
        return ItemTopic.objects.filter(topic=self).count()


    def numberCategories(self):
        return ItemTopic.objects.filter(topic=self).values('categories').distinct().count()



class ItemTopic(models.Model):
    STATUS = (('novo', 'Novo'),('ativo','Ativo'),('recusado','Recusado'))
    lemma = models.CharField(max_length=50)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, related_name='itemtopics', null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='novo')
    categories = models.ManyToManyField('CategoryBusiness')
    context = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.lemma

    def save(self, *args, **kwargs):
        super(ItemTopic, self).save(*args, **kwargs)
        if self.status == 'ativo': identify_all_opinion_by_lemma(self.lemma, self.topic)
        return self

    def get_admin_url(self):
        return '/admin/managedata/itemtopic/'+str(self.id)


class Opinion(models.Model):
    text_pt = models.CharField(max_length=500)
    text_en = models.CharField(max_length=500)
    lemmatized = models.CharField(max_length=500)
    polarity = models.IntegerField()
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='opinions')
    topics = models.ManyToManyField('Topic', blank=True)
    nouns = models.TextField(default='')


    def __str__(self):
        return self.text_pt


class BusinessPlan(models.Model):

    STATUS = (('solicitado','Solicitado'),('ativo','Ativo'),('cancelado','Cancelado'))
    description = models.CharField(max_length=240)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    enterprising = models.ForeignKey('Enterprising', on_delete=models.CASCADE)
    create_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS, default='solicitado')
    category = models.ForeignKey('CategoryBusiness', on_delete=models.CASCADE, related_name='business_plans')

    def ageDays(self):
        return (date.today() - self.create_date).days

    def location(self):
        return '%s, %s' % (self.city, self.state)


    def __str__(self):
        return '%s em %s de %s' % (self.category.specialty, self.city, self.enterprising)


class DataUpdate(models.Model):
    numero = models.IntegerField(unique=True)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    plans = models.ManyToManyField(BusinessPlan)


    class Meta:
        ordering = ['-numero']

    def timeInSeconds(self):
        return (self.datetime_end-self.datetime_start).seconds

    def __str__(self):
        return 'Update '+str(self.numero)



def identify_all_opinion_by_lemma(lemma, topic):
    opinions = Opinion.objects.filter(lemmatized__contains=lemma)
    for opinion in opinions:
        opinion.topics.add(topic)
    return opinions


