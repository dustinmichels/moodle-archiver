import shutil
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run():
    shutil.rmtree('output')
    process = CrawlerProcess(get_project_settings())
    process.crawl('moodle')
    process.start()


if __name__ == '__main__':
    run()
