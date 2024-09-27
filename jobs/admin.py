from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from jobs.models import Job

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    #定义展示字段和隐藏字段
    list_display = ('job_name','job_type','job_city','creator','create_date','modify_date')
    exclude = ('creator','create_date','modify_date')

    def save_model(self, request, obj, form, change) :
        obj.creator = request.user

        super().save_model(request, obj, form, change)# 用不用return都行
admin.site.register(Job, JobAdmin)