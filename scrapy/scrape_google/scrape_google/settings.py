# Scrapy settings for scrape_google project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrape_google'

SPIDER_MODULES = ['scrape_google.spiders']
NEWSPIDER_MODULE = 'scrape_google.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrape_google (+http://www.yourdomain.com)'
