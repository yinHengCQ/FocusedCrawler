#coding=utf-8
from __future__ import absolute_import

from celery import task
from service.urlopen.ganjiresume import download_ganji_data

import os,logging

__logger=logging.getLogger('django')


@task
def crawl_ganji_resume(list_str):
    __logger.info('city_codes:{0}'.format(list_str))
    for var in eval(list_str):
        download_ganji_data(var)