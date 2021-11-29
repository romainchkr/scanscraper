import logging
from scrapy.crawler import CrawlerProcess
from scanscraper.spiders import scanspider
from scrapy.utils.project import get_project_settings

from urllib.parse import urljoin
import os
from PIL import Image

class MyStaticCrawler:

    def __init__(self):
        self.output = None
        self.process = CrawlerProcess(get_project_settings())

    def yield_output(self, data):
        self.output = data

    def crawl(self, cls, urls):
        self.process.crawl(cls, start_urls=urls, args={'callback': self.yield_output})
        self.process.start()

def create_pdf(url):
    imageList = []
    # get png and jpg downloaded files
    files = os.listdir(url)
    files.sort()
    files = [file for file in files if '.jpg' in file or '.png' in file]

    if len(files) > 0:
        image1 = Image.open(url + files[0])
        for filename in files[1:]:
            imageList.append(Image.open(url + filename).convert('RGB'))
        
        image1.save(url + url.split('/')[-2] + '.pdf',save_all=True, append_images=imageList)

        delete_img(files)

def delete_img(files):
    pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    start_urls = ["https://www.scan-vf.net/solo-leveling", 'https://www.scan-vf.net/black-clover']

    crawler = MyStaticCrawler()
    crawler.crawl(scanspider.ScanSpider, start_urls)
    data = crawler.output
    logging.debug(data)

    for manga_name, chapters in data.items():
        for chapter in chapters:
            create_pdf(urljoin(os.getcwd(), 'scans/'+manga_name+'/'+chapter+'/'))