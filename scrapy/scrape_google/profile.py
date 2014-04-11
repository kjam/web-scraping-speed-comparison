import cProfile
from scrapy import cmdline
import pstats

cProfile.run('cmdline.execute("scrapy crawl google_results".split())','stats')
ps = pstats.Stats('stats')

print ps.print_stats(10)
