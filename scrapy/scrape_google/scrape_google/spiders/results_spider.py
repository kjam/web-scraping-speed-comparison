from scrapy.spider import Spider
from scrapy.selector import Selector
from urlparse import parse_qs
from scrape_google.items import ScrapeGoogleItem


class ResultsSpider(Spider):
    name = "google_results"
    allowed_domains = ['google.com']
    start_urls = ["http://www.google.com/search?q=python&start=%d" % r for r in range(360)[0::10]]

    def parse(self, response):
        sel = Selector(response)
        results = sel.xpath('//div[@id="center_col"]//ol/li')
        items = []
        for r in results:
            title = ''.join(r.xpath('h3/a//text()').extract())
            if len(r.xpath('h3/a/@href').extract()):
                link = parse_qs(r.xpath('h3/a/@href').
                                extract()[0].lstrip('/url?')).get('q')[0]
            else:
                continue
            desc = ''.join(r.xpath('div/span//text()').extract())
            item = ScrapeGoogleItem()
            item['title'] = title
            item['link'] = link
            item['desc'] = desc
            items.append(item)
        return items
