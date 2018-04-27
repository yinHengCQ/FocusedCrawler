#coding=utf-8
import time,re,logging,random
from lxml import etree
from service.models import ResumeGanji
from service.utils.disguiseUtil import get_random_pc_ua
from urllib.request import Request,urlopen


__logger=logging.getLogger('django')


def download_ganji_data(city_code):
    __logger.info('task ganji resume start...')
    start_time=time.time()
    for var in __get_base_urls(city_code):
        __download_ganji(var[0],var[1])
    __logger.info('task ganji resume finish,total time count:{0}'.format(time.time()-start_time))

def __get_base_urls(city_code):
    url="http://{0}.ganji.com/qiuzhi/###".format(city_code)
    headers = {
        'User-Agent': get_random_pc_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    request = Request(url=url, headers=headers)
    page = urlopen(request).read().decode('utf-8')
    base_urls=[]
    for var in etree.HTML(page).xpath('//div[@class="f-all-news"][1]/dl'):
        base_urls.append(('http://{0}.ganji.com{1}'.format(city_code,var.xpath('dt[1]/a[1]/@href')[0]),var.xpath('dt[1]/a[1]/text()')[0]))
    return base_urls


def __download_ganji(base_url,work_class):
    __logger.info('start download ganji resume,current base_url is:{0}'.format(base_url))
    start_time=time.time()
    try:
        for index in range(1,101):
            time.sleep(random.uniform(1,3))
            __download_ganji_resume('{0}o{1}/'.format(base_url,index),work_class)
    except Exception as error:
        __logger.error('download ganji resume error:{0}'.format(error))
    finally:
        __logger.info('task ganji resume finish,times count:{0}'.format(time.time()-start_time))

def __download_ganji_resume(url,work_class):
    # url = "http://cq.ganji.com/qzshichangyingxiao/o4/"
    headers = {
        'User-Agent': get_random_pc_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    request = Request(url=url, headers=headers)
    page = urlopen(request).read().decode('utf-8')
    __get_data(page,work_class)


def __trans_salary(hope_salary):
    try:
        temp=hope_salary.split('-')
        return {'low':re.sub('\D','',temp[0]),'high':re.sub('\D','',temp[1])}
    except:return {'low':'0','high':'0'}

def __get_data(page,work_class):
    path_list = etree.HTML(page).xpath('//div[@class="qz-resume-list"][1]/div[1]/dl')
    for var in path_list:
        # resume_id = var.xpath('a[1]/@post_id')[0]
        resume_id=var.xpath('div[1]/div[1]/input[1]/@value')[0][8:]
        name = var.xpath('a[1]/dt[1]/div[1]/div[1]/span[1]/text()')[0]
        sex = var.xpath('a[1]/dt[1]/div[1]/div[1]/span[2]/text()')[0]
        age = var.xpath('a[1]/dt[1]/div[1]/div[1]/span[3]/text()')[0]
        try:education = var.xpath('a[1]/dt[1]/div[1]/div[1]/span[4]/text()')[0]
        except:education=''
        try:work_age = var.xpath('a[1]/dt[1]/div[1]/div[1]/span[5]/text()')[0]
        except:work_age=''
        hope_job = re.sub('\s', '', var.xpath('a[1]/dt[1]/div[2]/div[2]/ul[1]/li[1]/text()')[0])
        hope_work_address = var.xpath('a[1]/dt[1]/div[2]/div[2]/ul[1]/li[2]/text()')[0]
        hope_salary = var.xpath('a[1]/dt[1]/div[2]/div[2]/ul[1]/li[3]/text()')[0]
        work_history_orgin = re.sub('\s', '', var.xpath('a[1]/dt[1]/div[2]/div[3]')[0].xpath('string(.)').strip())
        mark = u'{0}:{1}'.format(work_history_orgin[:work_history_orgin.find(u'份工作') + 3],work_history_orgin[work_history_orgin.find(u'份工作') + 3:])
        if mark==':':mark=''
        hope_salary_dict=__trans_salary(hope_salary)
        hope_salay_low=int(hope_salary_dict['low'])
        hope_salay_high = int(hope_salary_dict['high'])
        work_type=work_class

        try:ResumeGanji.objects.update_or_create(resume_id=resume_id,name=name,sex=sex,age=age,work_age=work_age,education=education,
                                              hope_job=hope_job,hope_work_address=hope_work_address,mark=mark,hope_salary=hope_salary,
                                                 hope_salay_low=hope_salay_low,hope_salay_high=hope_salay_high,work_type=work_type)
        except Exception as e:
            __logger.error('update_or_create ResumeGanji error:{0}'.format(e))
