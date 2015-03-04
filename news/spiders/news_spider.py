import scrapy
import requests

from lxml import html
from news.items import NewsItem

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = [
        "www.bloomberg.com",
        "www.bloombergview.com",
        "www.wsj.com"
    ]
    start_urls = [
        "http://www.bloomberg.com/news/world",
        "http://www.bloomberg.com/news/industries",
        "http://www.bloomberg.com/news/science-energy",
        "http://www.bloomberg.com/technology",
        "http://www.bloomberg.com/news/design",
        "http://www.bloomberg.com/news/culture",
        "http://www.bloomberg.com/graphics",
        "http://www.bloomberg.com/pursuits",
        "http://www.bloombergview.com",
        "http://www.bloomberg.com/politics",
        "http://www.bloomberg.com/businessweek"
    ]

    def parse(self, response):
        if response.url.find("wsj") == -1:
            for sel in response.xpath('//ul/li[@class="type-article"]'):
                if sel.xpath('h2/a/@href').extract():
                    item = NewsItem()
                    link = ''.join(sel.xpath('h2/a/@href').extract())
                    if link[:4] == "http":
                        item['link'] = link
                    else:
                        item['link'] = response.url[:response.url.index(".com")+4] + '/' + link
                    item['cate'] = response.url.split("/")[-1]
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
                    item['cate'] = response.url.split("/")[-1]
                    item['source'] = "bloomberg"
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
                        cate = response.url.split("/")[-1]
                        if cate.find('.html') != -1:
                            item['cate'] = cate[:cate.index(".html")]
                        else:
                            item['cate'] = cate
                        item['source'] = "wsj"
                        yield item
