# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpecificPageItem(scrapy.Item):
	name = scrapy.Field()
	url = scrapy.Field()
	description = scrapy.Field()
	rating = scrapy.Field()
	rateNum = scrapy.Field()
	developer = scrapy.Field()
	classification = scrapy.Field()
	uid = scrapy.Field()
