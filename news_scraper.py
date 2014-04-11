from lxml import html
from bs4 import BeautifulSoup
import cProfile
import pstats


page = open('data/nyt_mobile.html').read()


def run_lxml_xpath():
    all_news = []
    tree = html.document_fromstring(page)
    articles = tree.xpath('.//div[@id="articles"]')[0]
    for story in articles.xpath('ol/li'):
        title = story.xpath('a/span[@class="title"]//text()')
        link = story.xpath('a/@href')
        blurb = story.xpath('a/p//text()')
        all_news.append({
            'title': (lambda x: x[0] if len(x) else '')(title),
            'link': (lambda x: x[0] if len(x) else '')(link),
            'blurb': (lambda x: x[0] if len(x) else '')(blurb),
        })


def run_lxml_css():
    all_news = []
    tree = html.document_fromstring(page)
    articles = tree.cssselect('div#articles')[0]
    for story in articles.cssselect('ol li'):
        title = story.cssselect('span.title')
        link = story.find('a')
        blurb = story.cssselect('p')
        all_news.append({
            'title': (lambda x: x[0].text if len(x) else '')(title),
            'link': (lambda x: x[0].get('href')
                     if x is not None else '')(link),
            'blurb': (lambda x: x[0].text_content() if len(x) else '')(blurb),
        })


def run_beautiful_soup():
    all_news = []
    tree = BeautifulSoup(page)
    articles = tree.find('div', {'id': 'articles'})
    for story in articles.find_all('li'):
        title = story.find('span', {'class': 'title'})
        link = story.find('a')
        blurb = story.find('p')
        all_news.append({
            'title': (lambda x: x.text if x is not None else '')(title),
            'link': (lambda x: x.get('href') if x is not None else '')(link),
            'blurb': (lambda x: x.text if x is not None else '')(blurb),
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
    """print "Beautiful Soup!"
    cProfile.run('run_beautiful_soup()')
    print "LXML with CSS Select!"
    cProfile.run('run_lxml_css()')
    print "LXML with XPATH!"
    cProfile.run('run_lxml_xpath()')
    """
    averages = {"run_beautiful_soup()": {}, "run_lxml_css()": {},
                "run_lxml_xpath()": {}}

    for func in averages.keys():
        get_averages(func, averages, 500)
    print averages
