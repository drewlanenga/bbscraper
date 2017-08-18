# Scrapy settings for espn project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'espn'

SPIDER_MODULES = ['espn.spiders']
NEWSPIDER_MODULE = 'espn.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'espn (+http://www.yourdomain.com)'
