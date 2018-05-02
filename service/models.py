from django.db import models

# Create your models here.
class ResumeGanji(models.Model):
    resume_id=models.CharField(max_length=50)
    name=models.CharField(max_length=300,null=True)
    sex=models.CharField(max_length=5,null=True)
    age=models.CharField(max_length=10,null=True)
    work_age=models.CharField(max_length=50,null=True)
    education=models.CharField(max_length=100,null=True)
    hope_job=models.CharField(max_length=500,null=True)
    hope_work_address=models.CharField(max_length=300,null=True)
    mark=models.CharField(max_length=800,null=True)
    hope_salary=models.CharField(max_length=300,null=True)
    hope_salay_low=models.IntegerField(null=True)
    hope_salay_high=models.IntegerField(null=True)
    work_type=models.CharField(max_length=300,null=True)
    createTime=models.DateTimeField(auto_now_add=True,null=True)
    modifyTime=models.DateTimeField(auto_now=True)

class SohuNews(models.Model):
    id=models.CharField(primary_key=True,max_length=30)
    title=models.CharField(max_length=1024)
    publisher=models.CharField(max_length=1024)
    pub_date=models.CharField(max_length=1024)
    comment_count=models.CharField(max_length=32,default='0')
    url=models.CharField(max_length=1024)
    createTime=models.DateTimeField(auto_now_add=True,null=True)
    modifyTime=models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.title

class Job51(models.Model):
    job_id=models.CharField(max_length=50)
    job_name=models.CharField(max_length=1024,null=True)
    job_url=models.CharField(max_length=1024,null=True)
    company_name=models.CharField(max_length=1024,null=True)
    company_url=models.CharField(max_length=1024,null=True)
    job_address=models.CharField(max_length=100,null=True)
    job_salary=models.CharField(max_length=100,null=True)
    pub_date=models.CharField(max_length=50,null=True)
    salary_low=models.IntegerField(null=True)
    salary_high=models.IntegerField(null=True)
    createTime=models.DateTimeField(auto_now_add=True,null=True)
    modifyTime=models.DateTimeField(auto_now=True,null=True)


class Job51Detail(models.Model):
    job_id=models.CharField(max_length=50)
    job_name=models.CharField(max_length=1024,null=True)
    company_name=models.CharField(max_length=1024,null=True)
    company_desc=models.CharField(max_length=1024,null=True)
    job_jtag=models.CharField(max_length=1024,null=True)
    job_welfare=models.CharField(max_length=1024,null=True)
    job_detail_desc=models.CharField(max_length=10240,null=True)
    job_type_desc=models.CharField(max_length=1024,null=True)
    job_keyword_desc = models.CharField(max_length=1024,null=True)
    work_address=models.CharField(max_length=1024,null=True)
    createTime=models.DateTimeField(auto_now_add=True,null=True)
    modifyTime=models.DateTimeField(auto_now=True,null=True)