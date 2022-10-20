# Scrapy settings for TEDscraper2 project

BOT_NAME = 'TEDscraper2'

SPIDER_MODULES = ['TEDscraper2.spiders']
NEWSPIDER_MODULE = 'TEDscraper2.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
