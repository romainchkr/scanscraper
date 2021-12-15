import scrapy
from  scanscraper.items import ChapterItem

import logging
import os
import re
import json

# to execute the crawler uncomment line : start_urls ....
# then comment functions __init__ and close
# then launch the following command line : scrapy crawl scan 
class ScanSpider(scrapy.Spider):
    name = "scan"
    output = {}
    start_urls = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_callback = kwargs.get('args').get('callback')
    
    def close(self, spider, reason):
        self.output_callback(self.output)

    def parse(self, response):
        logging.info("Start scraping")

        manga_name = response.xpath('/html/body/div[1]/div/div[1]/div/h2/text()').get()
        if not os.path.exists("scans\\"+manga_name):
            os.makedirs("scans\\"+manga_name)
        
        self.output[manga_name] = []

        chapters = response.xpath('/html/body/div[1]/div/div[1]/div/div[4]/div/ul/li/h5/a/@href')
        #chapters = response.xpath('/html/body/div[1]/div/div[1]/div/div[4]/div/ul/li[1]/h5/a/@href')

        for chapter in chapters:
            logging.debug(chapter.get())
            yield scrapy.Request(chapter.get(), callback=self.parse_chapter, meta={'manga_name': manga_name})
    
    def parse_chapter(self, response):
        logging.debug("parse_chapter")

        images = re.search(r'var pages = \[.+\]',response.xpath("//script[contains(., 'var pages')]/text()").get()).group(0)
        image_obj = json.loads(images[images.index('['):])
        base = response.xpath('/html/body/div[1]/div[3]/div/div[2]/div[2]/a/img/@src').get()
        base_url = base[:len(base)-base[::-1].index('/')].strip()
        image_urls = [base_url + image['page_image'] for image in image_obj]

        chapter = image_urls[0].split('/')[-2].split('-')[1]
        yield ChapterItem(image_urls=image_urls, manga_name=response.meta.get('manga_name'), chapter=chapter)

        self.output[response.meta.get('manga_name')].append(chapter)