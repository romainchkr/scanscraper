import logging
from scrapy.crawler import CrawlerProcess
from scraper.spiders import scanspider
from scrapy.settings import Settings

from urllib.parse import urljoin
import os
from PIL import Image

class MyStaticCrawler:

    def __init__(self):
        self.output = None
        settings = Settings()
        settings.setmodule('scraper.settings', priority='project')
        self.process = CrawlerProcess(settings)

    def yield_output(self, data):
        self.output = data

    def crawl(self, cls, urls, chapters):
        self.process.crawl(cls, start_urls=urls, args={'callback': self.yield_output, 'chapters': chapters})
        self.process.start()

def create_pdf(url):
    imageList = []
    # get png and jpg downloaded files
    if os.path.exists(url) :
        files = os.listdir(url)
        files.sort()
        files = [url + file for file in files if '.jpg' in file or '.png' in file]

        if len(files) > 0:
            image1 = Image.open(files[0])
            for file in files[1:]:
                imageList.append(Image.open(file).convert('RGB'))
            
            image1.save(url + url.split('/')[-2] + '.pdf', save_all=True, append_images=imageList)

            delete_img(files)
    else :
        logging.info("Couldn't create PDF. link <%s> is not valid", url)

def delete_img(files):
    for file in files:
        os.remove(file)

def scrape(start_urls, chapters):
    crawler = MyStaticCrawler()
    crawler.crawl(scanspider.ScanSpider, start_urls, chapters)
    data = crawler.output

    for manga_name, chapters in data.items():
        for chapter in chapters:
            create_pdf(urljoin(os.getcwd(), 'scans/'+manga_name+'/'+chapter+'/'))