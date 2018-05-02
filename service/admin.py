from django.contrib import admin
from service.models import *

# Register your models here.


class resumeGanjiAdmin(admin.ModelAdmin):
    list_display = ['id','resume_id','name','sex','age','work_age','education','hope_job','hope_work_address','mark',
                    'hope_salary','hope_salay_low','hope_salay_high','work_type','createTime','modifyTime']

class sohuNewsAdmin(admin.ModelAdmin):
    list_display = ['id','title','publisher','pub_date','comment_count','url','createTime','modifyTime']


admin.site.register(ResumeGanji,resumeGanjiAdmin)
admin.site.register(SohuNews,sohuNewsAdmin)