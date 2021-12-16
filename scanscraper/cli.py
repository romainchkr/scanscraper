from argparse import ArgumentParser
import logging
from scraper.scanscraper import scrape

logging.basicConfig(level=logging.DEBUG)

#launch : python scanscraper --link https://www.scan-vf.net/solo-leveling
def main():
    parser = ArgumentParser(prog='scanscraper', description='Command line interface for the scanscraper app')

    parser.add_argument('--link', nargs='+', required=True, help="<Required> Link if the scans to scrape")   
    args = parser.parse_args()

    scrape(args.link)