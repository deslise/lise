from django.contrib import admin

# Register your models here.
from managedata.models import *

admin.site.register(Branch)
admin.site.register(CategoryBusiness)
admin.site.register(EarlyBusinessPlan)
admin.site.register(LateBusinessPlan)
admin.site.register(Business)
admin.site.register(Keyword)
admin.site.register(Opinion)
admin.site.register(Review)
admin.site.register(Topic)