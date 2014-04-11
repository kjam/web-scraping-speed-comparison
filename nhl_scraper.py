from lxml import html
from bs4 import BeautifulSoup
import cProfile
import pstats


page = open('data/hockey.html').read()


def run_lxml_xpath():
    all_scores = []
    tree = html.document_fromstring(page)
    scores = tree.xpath('.//div[@id="scoresBody"]')[0]
    for game in scores.xpath('.//div[contains(@class, "gamebox")]'):
        teams = [t.text for t in game.xpath(
            './/table//td/a') if t.text]
        totals = [g.text for g in game.xpath(
            './/table//td[contains(@class, "total")]')]
        all_scores.append(zip(teams, totals))


def run_lxml_css():
    all_scores = []
    tree = html.document_fromstring(page)
    scores = tree.cssselect('div#scoresBody')[0]
    for game in scores.cssselect('div.gamebox'):
        teams = [t.text_content() for t in game.cssselect('table td.team')]
        totals = [g.text for g in game.cssselect('table td.total')]
        all_scores.append(zip(teams, totals))


def run_beautiful_soup():
    all_scores = []
    tree = BeautifulSoup(page)
    scores = tree.find('div', {'id': 'scoresBody'})
    for game in scores.find_all('div', {'class': 'gamebox'}):
        teams = [t.text for t in game.find_all('td', {'class': 'team'})]
        totals = [tt.text for tt in game.find_all('td', {'class': 'total'})]
        all_scores.append(zip(teams, totals))


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
