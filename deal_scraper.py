from lxml import html
from bs4 import BeautifulSoup
import cProfile
import pstats


# In this example, Beautiful Soup could not locate the gbwshoveler-contnet
# divs so I was forced to utilize just the main deals on the page. It also
# did not present an accurate way of locating the prices in relation to
# those deals, so the price is omitted.


page = open('data/amazon_deals.html').read()


def run_lxml_xpath():
    all_deals = []
    tree = html.document_fromstring(page)
    deals = tree.xpath('.//div[@class="gbwshoveler-content"]')[0]
    for product in deals.xpath('ul/li'):
        title = product.xpath('.//div[@id="dealTitle"]//text()')
        price = product.xpath('.//span[@id="dealDealPrice"]//text()')
        link = product.xpath('.//div[@id="dealTitle"]/a/@href')
        all_deals.append({
            'title': (lambda x: x[0] if len(x) else '')(title),
            'price': (lambda x: x[0] if len(x) else '')(price),
            'link': (lambda x: x[0] if len(x) else '')(link),
        })


def run_lxml_css():
    all_deals = []
    tree = html.document_fromstring(page)
    deals = tree.cssselect('div.gbwshoveler-content')[0]
    for product in deals.cssselect('ul li'):
        title = product.cssselect('div#dealTitle')
        price = product.cssselect('span#dealDealPrice')
        link = product.cssselect('div#dealTitle a')
        all_deals.append({
            'title': (lambda x: x[0].text_content() if len(x) else '')(title),
            'price': (lambda x: x[0].text_content() if len(x) else '')(price),
            'link': (lambda x: x[0].get('href') if len(x) else '')(link),
        })


def run_beautiful_soup():
    all_deals = []
    tree = BeautifulSoup(page)
    deals = tree.find_all('div', {'id': 'dealTitle'})
    for product in deals:
        title = product.text
        link = product.find('a').get('href')
        all_deals.append({
            'title': title,
            'link': link,
        })


def get_averages(func, dict, rng):
    dict[func]['num_runs'] = 0.0
    dict[func]['ttl_calls'] = 0.0
    dict[func]['ttl_time'] = 0.0
    for i in range(rng):
        cProfile.run(func, 'stats')
        stats = pstats.Stats('stats')
        dict[func]['ttl_calls'] += stats.total_calls
        dict[func]['ttl_time'] += stats.total_tt
        dict[func]['num_runs'] += 1
    dict[func]['avg_time'] = dict[func]['ttl_time'] / dict[func]['num_runs']
    dict[func]['avg_calls'] = dict[func]['ttl_calls'] / dict[func]['num_runs']


if __name__ == '__main__':
    """
    print "Beautiful Soup!"
    cProfile.run('run_beautiful_soup()')
    print "LXML with CSS Select!"
    cProfile.run('run_lxml_css()')
    print "LXML with XPATH!"
    cProfile.run('run_lxml_xpath()')
    """
    averages = {"run_beautiful_soup()": {}, "run_lxml_css()": {},
                "run_lxml_xpath()": {}}

    for func in averages.keys():
        get_averages(func, averages, 10)
    print averages
