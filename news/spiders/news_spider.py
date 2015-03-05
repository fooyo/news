import scrapy
import requests

from lxml import html
from news.items import NewsItem
from dateutil.parser import parse

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = [
        "www.bloomberg.com",
        "www.bloombergview.com",
        "www.wsj.com"
    ]
    start_urls = [
        "http://www.bloomberg.com/news/world",
        "http://www.bloomberg.com/topics/united-states",
        "http://www.bloomberg.com/topics/europe",
        "http://www.bloomberg.com/topics/asia",
        "http://www.bloomberg.com/topics/australia",
        "http://www.bloomberg.com/topics/africa",
        "http://www.bloomberg.com/topics/latin-america",
        "http://www.bloomberg.com/topics/middle-east",
        "http://www.bloomberg.com/news/industries",
        "http://www.bloomberg.com/topics/auto-industry",
        "http://www.bloomberg.com/topics/tourism",
        "http://www.bloomberg.com/topics/health-care-industry",
        "http://www.bloomberg.com/topics/real-estate",
        "http://www.bloomberg.com/topics/wall-street",
        "http://www.bloomberg.com/topics/oil",
        "http://www.bloomberg.com/news/science-energy",
        "http://www.bloomberg.com/topics/health",
        "http://www.bloomberg.com/topics/climate",
        "http://www.bloomberg.com/topics/energy",
        "http://www.bloomberg.com/technology",
        "http://www.bloomberg.com/technology/companies",
        "http://www.bloomberg.com/topics/gadgets",
        "http://www.bloomberg.com/topics/startups",
        "http://www.bloomberg.com/topics/cybersecurity",
        "http://www.bloomberg.com/topics/video-games",
        "http://www.bloomberg.com/news/design",
        "http://www.bloomberg.com/topics/products",
        "http://www.bloomberg.com/topics/concepts",
        "http://www.bloomberg.com/topics/architecture",
        "http://www.bloomberg.com/topics/innovation",
        "http://www.bloomberg.com/topics/cities",
        "http://www.bloomberg.com/news/culture",
        "http://www.bloomberg.com/topics/entertainment",
        "http://www.bloomberg.com/topics/sports",
        "http://www.bloomberg.com/topics/food-industry",
        "http://www.bloomberg.com/topics/fashion",
        "http://www.bloomberg.com/topics/work",
        "http://www.bloomberg.com/politics/",
        "http://www.bloomberg.com/businessweek",
        "http://www.bloomberg.com/topics/cover-story",
        "http://www.bloomberg.com/topics/opening-remarks",
        "http://www.bloomberg.com/topics/features",
        "http://www.wsj.com/public/page/news-global-world.html",
        "http://www.wsj.com/public/page/news-world-business.html",
        "http://www.wsj.com/public/page/news-business-us.html",
        "http://www.wsj.com/news/technology",
        "http://www.wsj.com/public/page/news-financial-markets-stock.html",
        "http://www.wsj.com/public/page/news-personal-finance.html",
        "http://www.wsj.com/public/page/new-york-main.html",
        "http://www.wsj.com/public/page/news-opinion-commentary.html",
        "http://www.wsj.com/public/page/news-real-estate-homes.html",
        "http://www.wsj.com/public/page/management.html",
        "http://www.wsj.com/public/page/news-asia-business.html",
        "http://www.wsj.com/public/page/hk-news.html",
        "http://www.wsj.com/public/page/news-china.html",
        "http://www.wsj.com/public/page/news-india.html",
        "http://www.wsj.com/public/page/news-japan.html",
        "http://www.wsj.com/public/page/sea.html",
        "http://www.wsj.com/public/page/news-european-union.html",
        "http://www.wsj.com/public/page/uk.html",
        "http://www.wsj.com/public/page/russia.html",
        "http://www.wsj.com/public/page/news-africa.html",
        "http://www.wsj.com/public/page/mideast.html",
        "http://www.wsj.com/public/page/news-canada.html",
        "http://www.wsj.com/public/page/news-latin-america.html",
        "http://www.wsj.com/public/page/news-earnings.html",
        "http://www.wsj.com/public/page/news-economy.html",
        "http://www.wsj.com/public/page/news-transportation-industry.html",
        "http://www.wsj.com/public/page/news-arts-movies-music.html",
        "http://www.wsj.com/public/page/news-watches-jewelry.html",
        "http://www.wsj.com/public/page/news-fashion-style-industry.html",
        "http://www.wsj.com/public/page/news-food-cooking-drink.html",
        "http://www.wsj.com/public/page/consumer-health-wellness.html",
        "http://www.wsj.com/public/page/news-sports-scores.html",
        "http://www.wsj.com/public/page/news-travel-vacation.html"
        "http://www.wsj.com/public/page/book-reviews.html",
        "http://www.wsj.com/public/page/letters.html",
        "http://www.wsj.com/public/page/leisure-arts.html"
    ]
    def parse(self, response):
        categoryMap = {
            "http://www.bloomberg.com/news/world": "world",
            "http://www.bloomberg.com/topics/united-states": "world",
            "http://www.bloomberg.com/topics/europe": "world",
            "http://www.bloomberg.com/topics/asia": "world",
            "http://www.bloomberg.com/topics/australia": "world",
            "http://www.bloomberg.com/topics/africa": "world",
            "http://www.bloomberg.com/topics/latin-america": "world",
            "http://www.bloomberg.com/topics/middle-east": "world",
            "http://www.bloomberg.com/news/industries": "industries",
            "http://www.bloomberg.com/topics/auto-industry": "industries",
            "http://www.bloomberg.com/topics/tourism": "industries",
            "http://www.bloomberg.com/topics/health-care-industry": "industries",
            "http://www.bloomberg.com/topics/real-estate": "finance",
            "http://www.bloomberg.com/topics/wall-street": "finance",
            "http://www.bloomberg.com/topics/oil": "industries",
            "http://www.bloomberg.com/news/science-energy": "science",
            "http://www.bloomberg.com/topics/health": "science",
            "http://www.bloomberg.com/topics/climate": "science",
            "http://www.bloomberg.com/topics/energy": "science",
            "http://www.bloomberg.com/technology": "technology",
            "http://www.bloomberg.com/technology/companies": "technology",
            "http://www.bloomberg.com/topics/gadgets": "technology",
            "http://www.bloomberg.com/topics/startups": "technology",
            "http://www.bloomberg.com/topics/cybersecurity": "technology",
            "http://www.bloomberg.com/topics/video-games": "technology",
            "http://www.bloomberg.com/news/design": "design",
            "http://www.bloomberg.com/topics/products": "design",
            "http://www.bloomberg.com/topics/concepts": "design",
            "http://www.bloomberg.com/topics/architecture": "design",
            "http://www.bloomberg.com/topics/innovation": "design",
            "http://www.bloomberg.com/topics/cities": "design",
            "http://www.bloomberg.com/news/culture": "culture",
            "http://www.bloomberg.com/topics/entertainment": "culture",
            "http://www.bloomberg.com/topics/sports": "culture",
            "http://www.bloomberg.com/topics/food-industry": "culture",
            "http://www.bloomberg.com/topics/fashion": "culture",
            "http://www.bloomberg.com/topics/work": "culture",
            "http://www.bloomberg.com/politics/": "politics",
            "http://www.bloomberg.com/businessweek": "business",
            "http://www.bloomberg.com/topics/cover-story": "business",
            "http://www.bloomberg.com/topics/opening-remarks": "business",
            "http://www.bloomberg.com/topics/features": "business",
            "http://www.wsj.com/public/page/news-global-world.html": "world",
            "http://www.wsj.com/public/page/news-world-business.html": "business",
            "http://www.wsj.com/public/page/news-business-us.html": "business",
            "http://www.wsj.com/news/technology": "technology",
            "http://www.wsj.com/public/page/news-financial-markets-stock.html": "finance",
            "http://www.wsj.com/public/page/news-personal-finance.html": "finance",
            "http://www.wsj.com/public/page/news-opinion-commentary.html": "opinion",
            "http://www.wsj.com/public/page/news-real-estate-homes.html": "finance",
            "http://www.wsj.com/public/page/management.html": "management",
            "http://www.wsj.com/public/page/news-asia-business.html": "world",
            "http://www.wsj.com/public/page/hk-news.html": "world",
            "http://www.wsj.com/public/page/news-china.html": "world",
            "http://www.wsj.com/public/page/news-india.html": "world",
            "http://www.wsj.com/public/page/news-japan.html": "world",
            "http://www.wsj.com/public/page/sea.html": "world",
            "http://www.wsj.com/public/page/news-european-union.html": "world",
            "http://www.wsj.com/public/page/uk.html": "world",
            "http://www.wsj.com/public/page/russia.html": "world",
            "http://www.wsj.com/public/page/news-africa.html": "world",
            "http://www.wsj.com/public/page/mideast.html": "world",
            "http://www.wsj.com/public/page/news-canada.html": "world",
            "http://www.wsj.com/public/page/news-latin-america.html": "world",
            "http://www.wsj.com/public/page/news-earnings.html": "business",
            "http://www.wsj.com/public/page/news-economy.html": "business",
            "http://www.wsj.com/public/page/news-transportation-industry.html": "business",
            "http://www.wsj.com/public/page/news-arts-movies-music.html": "culture",
            "http://www.wsj.com/public/page/news-watches-jewelry.html": "culture",
            "http://www.wsj.com/public/page/news-fashion-style-industry.html": "culture",
            "http://www.wsj.com/public/page/news-food-cooking-drink.html": "culture",
            "http://www.wsj.com/public/page/consumer-health-wellness.html": "culture",
            "http://www.wsj.com/public/page/news-sports-scores.html": "culture",
            "http://www.wsj.com/public/page/news-travel-vacation.html": "culture",
            "http://www.wsj.com/public/page/book-reviews.html": "opinion",
            "http://www.wsj.com/public/page/letters.html": "opinion",
            "http://www.wsj.com/public/page/leisure-arts.html": "opinion"
        }
        if response.url.find("wsj") == -1:
            for sel in response.xpath('//ul/li[@class="type-article"]'):
                if sel.xpath('h2/a/@href').extract():
                    item = NewsItem()
                    link = ''.join(sel.xpath('h2/a/@href').extract())
                    if link[:4] == "http":
                        item['link'] = link
                    else:
                        item['link'] = response.url[:response.url.index(".com")+4] + '/' + link
                    item['cate'] = categoryMap[response.url]
                    f = requests.get(item['link'])
                    parsed_body = html.fromstring(f.text)
                    body = parsed_body.xpath('//section[@class="article-body"]/descendant::*/text()')
                    if body:
                        item['body'] = ''.join(body)
                    else:
                        body = parsed_body.xpath('//div[@class="video-info__summary"]/text()')
                        if body:
                            item['body'] = ''.join(body)
                        else:
                            item['body'] = ""
                    item['img'] = parsed_body.xpath('//figure/img/@src')
                    time = parsed_body.xpath('//time/text()')
                    if time:
                        try:
                            item['time'] = parse(''.join(time).strip())
                        except ValueError:
                            item['time'] = ""
                    else:
                        item['time'] = ""
                    title = parsed_body.xpath('//h1/span/text()')
                    if title:
                        item['title'] = ''.join(title)
                    else:
                        title = parsed_body.xpath('//h1[@class="video-info__headline"]/text()')
                        if title:
                            item['title'] = ''.join(title)
                        else:
                            item['title'] = ""
                    item['source'] = "bloomberg"
                    yield item
            for sel in response.xpath('//h1/a'):
                if sel.xpath('@href').extract():
                    item = NewsItem()
                    link = ''.join(sel.xpath('@href').extract())
                    if link[:4] == "http":
                        item['link'] = link
                    else:
                        item['link'] = response.url[:response.url.index(".com")+4] + '/' + link
                    f = requests.get(item['link'])
                    parsed_body = html.fromstring(f.text)
                    body = parsed_body.xpath('//section[@class="article-body"]/descendant::*/text()')
                    if body:
                        item['body'] = ''.join(body)
                    else:
                        body = parsed_body.xpath('//div[@class="video-info__summary"]/text()')
                        if body:
                            item['body'] = ''.join(body)
                        else:
                            item['body'] = ""
                    title = parsed_body.xpath('//h1/span/text()')
                    if title:
                        item['title'] = ''.join(title)
                    else:
                        title = parsed_body.xpath('//h1[@class="video-info__headline"]/text()')
                        if title:
                            item['title'] = ''.join(title)
                        else:
                            item['title'] = ""
                    item['img'] = parsed_body.xpath('//figure/img/@src')
                    item['cate'] = categoryMap[response.url]
                    item['source'] = "bloomberg"
                    time = parsed_body.xpath('//time/text()')
                    if time:
                        try:
                            item['time'] = parse(''.join(time).strip())
                        except ValueError:
                            item['time'] = ""
                    else:
                        item['time'] = ""
                    yield item
        else:
            for sel in response.xpath('//ul/li'):
                if sel.xpath('h2/a/text()').extract():
                    item = NewsItem()
                    title = sel.xpath('h2/a/text()').extract()
                    item['title'] = ''.join(title)
                    link = ''.join(sel.xpath('h2/a/@href').extract())
                    if link[:4] == "http":
                        item['link'] = link
                    else:
                        item['link'] = response.url[:response.url.index(".com")+4] + '/' + link
                    if item['link'][:20] != "http://blogs.wsj.com":
                        f = requests.get(item['link'])
                        parsed_body = html.fromstring(f.text)
                        img = parsed_body.xpath('//div[@class="image-container"]/img/@src')
                        if img:
                            item['img'] = img
                        else:
                            item['img'] = sel.xpath('div/a/img/@src').extract()
                        body = parsed_body.xpath('//div[@class="wsj-snippet-body"]/descendant::*/text()')
                        if body:
                            item['body'] = ''.join(body)
                        else:
                            body = parsed_body.xpath('//div[@class="article-wrap"]/p/text()')
                            if body:
                                item['body'] = ''.join(body)
                            else:
                                item['body'] = ""
                        time = parsed_body.xpath('//time/text()')
                        if time:
                            try:
                                item['time'] = parse(''.join(time).strip())
                            except ValueError:
                                item['time'] = ""
                        else:
                            item['time'] = ""
                        item['cate'] = categoryMap[response.url]
                        item['source'] = "wsj"
                        yield item
