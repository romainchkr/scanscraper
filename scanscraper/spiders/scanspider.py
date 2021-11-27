import scrapy
import logging
import os
import re
import json

# execute script : scrapy crawl scan 
class ScanSpider(scrapy.Spider):
    name = "scan"
    start_urls = ["https://www.scan-vf.net/dr-stone"]

    def parse(self, response):
        logging.info("Starting scrape")

        manga_name = response.xpath('/html/body/div[1]/div/div[1]/div/h2/text()').get()
        if not os.path.exists("Scans\\"+manga_name):
            os.makedirs("Scans\\"+manga_name)

        chapters = response.xpath('/html/body/div[1]/div/div[1]/div/div[4]/div/ul/li/h5/a/@href')

        for chapter in chapters:
            logging.debug(chapter.get())
            yield scrapy.Request(chapter.get(), callback=self.parse_chapter)

    def parse_chapter(self, response):
        logging.debug("parse_chapter")

        images = re.search(r'var pages = \[.+\]',response.xpath("//script[contains(., 'var pages')]/text()").get()).group(0)
        image_obj = json.loads(images[images.index('['):])
        base = response.xpath('/html/body/div[1]/div[3]/div/div[2]/div[2]/a/img/@src').get()
        base_url = base[:len(base)-base[::-1].index('/')].strip()
        image_urls = [base_url + image['page_image'] for image in image_obj]

        yield {
            'image_urls' : image_urls
        }