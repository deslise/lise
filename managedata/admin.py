from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Permission

from managedata.models import *

admin.site.register(Branch)
admin.site.register(CategoryBusiness)
admin.site.register(BusinessPlan)
admin.site.register(Business)
admin.site.register(Keyword)
admin.site.register(Opinion)
admin.site.register(Review)
admin.site.register(Topic)
admin.site.register(ItemTopic)
admin.site.register(Enterprising)
admin.site.register(Weekday)
admin.site.register(RequestCategory)
admin.site.register(Permission)