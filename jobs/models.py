from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.

JobTypes = [
    (8,"技术类"),
    (1,"产品类"),
    (2,"运营类"),
    (3,"设计类"),



]

Cities = [
    (0,"北京"),
    (1,"上海"),
    (2,"深圳"),


]


# 候选人学历
DEGREE_TYPE = ((u'本科', u'本科'), (u'硕士', u'硕士'), (u'博士', u'博士'))



class Job(models.Model):
    job_type = models.SmallIntegerField(blank=False, choices=JobTypes, verbose_name=_("职位类别"))
    job_name = models.CharField(max_length=250, blank=False, verbose_name=_("职位名称")) #字符串
    job_city = models.SmallIntegerField(choices=Cities, blank=False, verbose_name=_("工作地点"))
    job_reponsibility = models.TextField(max_length = 1024,verbose_name = "职位职责") # 长文本
    job_requirement = models.TextField(max_length = 1024,blank = False, verbose_name = "职位要求") # 长文本
    creator = models.ForeignKey(User,verbose_name = "创建人",null=True, on_delete=models.SET_NULL) # 导入进来 要考虑到删除的情况
    create_date = models.DateTimeField(verbose_name = "创建日期",default = datetime.now)
    modify_date = models.DateTimeField(verbose_name = "修改日期")

    # 要把model注册到管理后台
    # 然后同步数据库


