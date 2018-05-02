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