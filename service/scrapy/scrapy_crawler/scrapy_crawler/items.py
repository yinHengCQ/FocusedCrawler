# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Job51CrawlerItem(scrapy.Item):
    job_id=scrapy.Field()
    job_name=scrapy.Field()
    job_url=scrapy.Field()
    company_name=scrapy.Field()
    company_url=scrapy.Field()
    job_address=scrapy.Field()
    job_salary=scrapy.Field()
    pub_date=scrapy.Field()
    salary_low=scrapy.Field()
    salary_high=scrapy.Field()
    company_desc=scrapy.Field()
    job_jtag=scrapy.Field()
    job_welfare=scrapy.Field()
    job_detail_desc=scrapy.Field()
    job_type_desc=scrapy.Field()
    job_keyword_desc = scrapy.Field()
    work_address=scrapy.Field()