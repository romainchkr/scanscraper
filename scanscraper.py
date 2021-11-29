from scrapy.crawler import CrawlerProcess
from scanscraper.spiders import scanspider
from scrapy.utils.project import get_project_settings

from urllib.parse import urljoin
import os
from PIL import Image

def create_pdf():
    imageList = []
    base_url = urljoin(os.getcwd(), 'scans/Solo Leveling/')
    folders = os.listdir(base_url)

    for folder in folders:
        files_url = urljoin(os.getcwd(), 'scans/Solo Leveling/'+folder+'/')
        files = os.listdir(files_url)
        files.sort()
        files = [file for file in files if '.jpg' in file or '.png' in file]

        if len(files) > 0:
            image1 = Image.open(files_url + files[0])
            for filename in files[1:]:
                imageList.append(Image.open(files_url + filename).convert('RGB'))
            
            image1.save(files_url + folder + '.pdf',save_all=True, append_images=imageList)
            delete_img(files)

def delete_img(files):
    pass

if __name__ == '__main__':
    start_urls = ["https://www.scan-vf.net/solo-leveling"]

    process = CrawlerProcess(get_project_settings())
    process.crawl(scanspider.ScanSpider, start_urls=start_urls)
    process.start()

    create_pdf()