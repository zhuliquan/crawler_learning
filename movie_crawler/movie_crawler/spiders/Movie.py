# -*- coding: utf-8 -*-
import scrapy
from movie_crawler.items import MovieCrawlerItem


class MovieSpider(scrapy.Spider):
    name = 'Movie'
    allowed_domains = ['meijutt.com']
    start_urls = ['http://www.meijutt.com/new100.html']

    def parse(self, response):
        movies = response.xpath('//ul[@class="top-list  fn-clear"]/li')
        for each_movie in movies:
            item = MovieCrawlerItem()
            item['name'] = each_movie.xpath('./h5/a/@title').extract()[0]
            yield item
