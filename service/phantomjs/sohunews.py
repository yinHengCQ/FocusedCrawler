#coding=utf-8
from service.utils.disguiseUtil import get_random_pc_ua
from service.models import SohuNews
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging,time,re
from lxml import etree



__logger=logging.getLogger('django')

def download_sohu_news():
    start_time=time.time()
    __logger.info("crawl sohu news start...")
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
    dcap["phantomjs.page.settings.userAgent"] = get_random_pc_ua()
    driver = webdriver.PhantomJS(executable_path=r'C:\Users\phantomjs-2.1.1-windows\bin\phantomjs.exe',desired_capabilities=dcap)  # 加载网址
    driver.set_page_load_timeout(15)

    try:
        driver.get("http://business.sohu.com/")
        time.sleep(1)
        __save_news(driver.page_source)
    except Exception as error:__logger.error("sohu news crawler error:{0}".find(error))
    finally:
        driver.quit()
        __logger.info("crawl sohu news finish,total times count:{0}".format(time.time()-start_time))

def __save_news(page):
    temp = etree.HTML(page).xpath('//div[@class="news-wrapper"]/div[@data-role="news-item"]')
    for var in temp:
        try:
            news_url = 'http:{0}'.format(var.xpath('h4/a[1]/@href')[0])
            news_id = re.sub('\D', '', news_url)
            news_title = var.xpath('h4/a[1]/text()')[0]
            news_publisher = var.xpath('div/span[@class="name"]/a[1]/text()')[0]
            comment_count = var.xpath('div/a[@class="com"]/span[1]/text()')[0]
            pub_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(var.xpath('div/span[@class="time"]/@data-val')[0]) / 1000))

            try:
                orgin = SohuNews.objects.get(id=news_id)
                orgin.comment_count = comment_count
                orgin.save()
            except SohuNews.DoesNotExist:
                SohuNews.objects.create(id=news_id, title=news_title, url=news_url, publisher=news_publisher,comment_count=comment_count, pub_date=pub_date)
        except Exception as e:__logger.error("save sohu news error:{0}".format(e))


