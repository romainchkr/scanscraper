from argparse import ArgumentParser
from scraper.scanscraper import scrape

import logging

MAX_CHAPTER_NUMBER = 1999

#launch : python scanscraper --link https://www.scan-vf.net/solo-leveling
def main():
    parser = ArgumentParser(prog='scanscraper', description='Command line interface for the scanscraper app')

    parser.add_argument('-l', '--link', type=str, nargs='+', required=True, help="<Required> Link if the scans to scrape")   
    parser.add_argument('-c', '--chapter', nargs='+', default=['0-'], help="Chapters to scrape")
    parser.add_argument('-L', '--loglevel', type=str, default="WARNING", choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], help="Log level of the scraper")
    args = parser.parse_args()

    #parse chapter
    chapters = []
    for chapter in args.chapter:
        if '-' in chapter:
            numbers = chapter.split('-')
            if len(numbers) == 2 and numbers[0] != '' and numbers[1] != '':
                try:
                    min = int(numbers[0])
                    if numbers[1] == '*':
                        max = MAX_CHAPTER_NUMBER
                    else:
                        max = int(numbers[1])
                    
                    if min>max:
                        raise ValueError

                    if min<0 or max<0:
                        raise TypeError

                    for i in range(min, max+1):
                        chapters.append(i)

                except TypeError:
                    parser.error(f"chapters must be positive integers {min}-{max}")
                except ValueError:
                    parser.error(f"bad boundaries for the chapter range {numbers[0]}-{numbers[1]}")
                except:
                    parser.error("chapter range must contain integers")
            else:
                parser.error(f"{chapter} is not a valid chapter")
        else:
            try:
                chapters.append(int(chapter))
            except:
                parser.error("chapter type must be positive integers") 
            
    #remove duplicate chapters
    chapters = list(dict.fromkeys(chapters))
    scrape(args.link, chapters, args.loglevel)