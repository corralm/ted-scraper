import json
import scrapy


class TEDscraper(scrapy.Spider):
    name = 'TEDscraper'
    start_urls = [
        # 'https://www.ted.com/talks?page=1'
        f'https://www.ted.com/talks?page={i}' for i in range(1, 160)
    ]

    def parse(self, response):
        talks_page_links = response.xpath("//a[@class=' ga-link']/@href")
        yield from response.follow_all(talks_page_links, self.parse_talk)

        # pagination_links = response.css(".pagination__next")
        # yield from response.follow_all(pagination_links, self.parse)

    
    def parse_talk(self, response): 
        raw = response.xpath("//script[@type='application/json']/text()").get()
        js = json.loads(raw)
        d = js['props']['pageProps']['videoData']
        yield {
            'talk_id': d['id'],
            'title': d['title'],
            'speaker': d['presenterDisplayName'],
            'recorded_date': d['recordedOn'],
            'published_date': d['publishedAt'],
            'event': d['videoContext'],
            'duration': d['duration'],
            'views': d['viewedCount'],
            'likes': response.css('.items-center span').re_first('->(.+)<!')
        }
 