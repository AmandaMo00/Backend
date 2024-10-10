import csv
from datetime import datetime
import logging
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from interview.models import Candidate

# Register your models here.
logger = logging.getLogger(__name__)



exportable_fields =  ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result', 'first_interviewer_user',
                     'second_result', 'second_interviewer_user', 'hr_result', 'hr_score', 'hr_remark', 'hr_interviewer_user')



# define export action
def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv') # http对象？
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=%s-list-%s.csv' % (
        'recruitment-candidates',
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    # 写入表头
    writer = csv.writer(response)
    writer.writerow(       
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list],
    )

    for obj in queryset:
        ## 单行 的记录（各个字段的值）， 根据字段对象，从当前实例 (obj) 中获取字段值
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
    logger.error(" %s has exported %s candidate records" % (request.user.username, len(queryset)))

    return response

export_model_as_csv.short_description = u'导出为CSV文件'

export_model_as_csv.allowed_permissions = ('export',)





# 候选人管理类
class CandidateAdmin(admin.ModelAdmin):
    #不展示字段
    exclude = ('creator', 'created_date', 'modified_date')

    list_display = (
    'username', 'city', 'bachelor_school', 'first_score', 'first_result', 'first_interviewer_user', 'second_result',
    'second_interviewer_user', 'hr_score', 'hr_result', 'last_editor',)

    list_filter = ('city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user', 'second_interviewer_user', 'hr_interviewer_user')

    # 查询字段

    search_fields = ("username", "city", "phone","bachelor_school",)


    # 排序字段
    ordering = ( 'hr_result', 'second_result', 'first_result' ) 
    # 增加actions
    actions = [export_model_as_csv,]

    # 当前用户是否有导出权限：
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))





    # 分组展示字段，分三块，基础信息，第一轮面试记录。。。
    fieldsets = (
        (None, {'fields': ("userid", ("username", "city", "phone"), ("email", "apply_position", "born_address", "gender", "candidate_remark"), ("bachelor_school", "master_school", "doctor_school"), ("major", "degree"), ("test_score_of_general_ability", "paper_score"),)}),
        ('第一轮面试', {'fields': (("first_score", "first_learning_ability", "first_professional_competency"), "first_advantage", "first_disadvantage", "first_result", "first_interviewer_user", "first_remark",)}),
        ('第二轮面试（专业复试）', {'fields': (("second_score", "second_learning_ability", "second_professional_competency"),("second_pursue_of_excellence", "second_communication_ability", "second_pressure_score"), "second_advantage", "second_disadvantage", "second_result", "second_interviewer_user", "second_remark",)}),
        ('HR复试', {'fields': ("hr_score", ("hr_responsibility", "hr_communication_ability", "hr_logic_ability"), ("hr_potential", "hr_stability"), "hr_advantage", "hr_disadvantage", "hr_result", "hr_interviewer_user", "hr_remark",)}),
        )
    
    # 应聘者看面试官信息是只读权限,但是这个是所有人都是只读
    # readonly_fields = ('first_interviewer_user', 'second_interviewer_user',)

    # 用这个来设置部分人只读

    def get_group_names(self,user):
        # 拿到所有的名字
        group_names =[]
        for g in user.groups.all():
            group_names.append(g.name) 
        return group_names
    
    def get_readonly_fields(self, request, obj ) :

        group_names = self.get_group_names(request.user)
        if 'interviewer' in group_names:
            logger.info("interviewer is in user;s group for %s" % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # 如果用户是超级用户允许查看所有数据
        if request.user.groups.filter(name = "interviewer").exists():
          
            print("Current User:", request.user.username)

            return qs.filter(username=request.user)  # 这个名字需要想清楚是什么

        # logger.info(f'{request.user.username} is NOT in the interviewer group')
        print('1')
        return qs
 
admin.site.register(Candidate, CandidateAdmin)
