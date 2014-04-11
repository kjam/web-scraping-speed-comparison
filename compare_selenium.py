from selenium import webdriver
import cProfile
import pstats

browser = webdriver.Firefox()
browser.get('http://yahoo.com')


def find_with_xpath():
    trends = []
    search = browser.find_element_by_xpath('.//input')
    trending = browser.find_elements_by_xpath(
        './/ol[contains(@class, "trendingnow_trend-list")]/li/a')
    trends = [a.text for a in trending]


def find_with_css():
    search = browser.find_element_by_class_name('input-query')
    trending = browser.find_elements_by_class_name("trendingnow_trend-list")
    trends = [a.text for a in trending]


def find_with_tag():
    search = browser.find_element_by_tag_name('input')
    trending = browser.find_element_by_tag_name(
        'ol').find_elements_by_tag_name('li')
    trends = [a.text for a in trending]


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

    averages = {"find_with_xpath()": {}, "find_with_css()": {},
                "find_with_tag()": {}}

    for func in averages.keys():
        get_averages(func, averages, 10)
    print averages
