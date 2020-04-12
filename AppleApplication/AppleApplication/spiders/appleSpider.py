# -*- coding: utf-8 -*-
import scrapy
from urllib import urlencode
from scrapy.http.request import Request


from AppleApplication.items import SpecificPageItem

class ApplespiderSpider(scrapy.Spider):
	name = 'appleSpider'
	allowed_domains = ['apple.com']
	start_urls = ['https://apps.apple.com/us/genre/ios-books/id6018',
	'https://apps.apple.com/us/genre/ios-business/id6000',
	'https://apps.apple.com/us/genre/ios-developer-tools/id6026',
	'https://apps.apple.com/us/genre/ios-education/id6017',
	'https://apps.apple.com/us/genre/ios-entertainment/id6016',
	'https://apps.apple.com/us/genre/ios-finance/id6015',
	'https://apps.apple.com/us/genre/ios-food-drink/id6023',
	'https://apps.apple.com/us/genre/ios-games/id6014',
	'https://apps.apple.com/us/genre/ios-graphics-design/id6027',
	'https://apps.apple.com/us/genre/ios-health-fitness/id6013',
	'https://apps.apple.com/us/genre/ios-lifestyle/id6012',
	'https://apps.apple.com/us/genre/ios-magazines-newspapers/id6021',
	'https://apps.apple.com/us/genre/ios-medical/id6020',
	'https://apps.apple.com/us/genre/ios-music/id6011',
	'https://apps.apple.com/us/genre/ios-navigation/id6010',
	'https://apps.apple.com/us/genre/ios-news/id6009',
	'https://apps.apple.com/us/genre/ios-photo-video/id6008',
	'https://apps.apple.com/us/genre/ios-productivity/id6007',
	'https://apps.apple.com/us/genre/ios-reference/id6006',
	'https://apps.apple.com/us/genre/ios-shopping/id6024',
	'https://apps.apple.com/us/genre/ios-social-networking/id6005',
	'https://apps.apple.com/us/genre/ios-sports/id6004',
	'https://apps.apple.com/us/genre/ios-travel/id6003',
	'https://apps.apple.com/us/genre/ios-utilities/id6002',
	'https://apps.apple.com/us/genre/ios-weather/id6001'
	]

	def start_requests(self):
		headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
		for url in self.start_urls:
			item = {}
			item['name'] = url.split('/')[5]
			item['url'] = url
			yield Request(url, meta={'item':item},callback=self.parseItemTop, headers=headers)
	

	def parseItemTop(self, response):

		item = response.meta['item']
		currentUrl = response.url

		data = response.xpath('//div[@id="selectedcontent"]//li//a')
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

		for letterNum in range(26):
			currentLetter = chr(letterNum + 65)
			for pageNum in range(1, 21):
				params = {'letter':currentLetter,'page':pageNum}
				yield Request(
					url = currentUrl + '?letter='+currentLetter+'&page=' + str(pageNum) + '#page',
					callback = self.parseClassPage,
					meta={'item':item}
					)
		return

	def parseClassPage(self, response):
		data = response.xpath('//div[@id="selectedcontent"]//li//a')
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

		for i in data:
			specificPageUrl = i.attrib['href']
			yield Request(
				url = specificPageUrl,
				callback = self.parseSpecificPage,
				meta = response.meta,
				headers = headers
				)
		return

	def parseSpecificPage(self, response):

		item = response.meta['item']

		# The name of the app
		name = response.xpath('//h1[@class="product-header__title app-header__title"]//text()').get()
		name = name.strip(' \n')
		if not name:
			name = "No name?"
		
		# The developer of the app
		developerSelec = response.xpath('//h2[@class="product-header__identity app-header__identity"]//a//text()')
		developer = ''
		if developerSelec:
			developer = developerSelec[0].get()
			developer = developer.strip(' \n\t')
		if not developer:
			developer = 'Unknown'

		# The rating of the app
		ratingSelec = response.xpath('//figcaption[@class="we-rating-count star-rating__count"]//text()')
		rating, rateNum = "0", "0"
		if ratingSelec:
			rating, rateNum = ratingSelec.get().split(',')
			rating = str(rating)
			rateNum = rateNum.split(' ')[0]
		if not rateNum:
			rateNum = "0"
		if not rating:
			rating = "0"

		# The description of the app
		descriptionSelec = response.xpath('//div[@class="section__description"]//p')
		description = ""
		if descriptionSelec:
			text = descriptionSelec.get()
			description = text.replace('<br>', ' ').strip()
		if not description:
			description = "EMPTY"

		pageItem = SpecificPageItem()
		pageItem['description'] = description
		pageItem['name'] = name
		pageItem['url'] = response.url
		pageItem['rating'] = rating
		pageItem['rateNum'] = rateNum
		pageItem['developer'] = developer
		pageItem['classification'] = response.meta['item']['name']
		pageItem['uid'] = response.url.split('/')[-1][2:]
		yield pageItem


#API key is a71feaad4aeec7b6a1f8aa80008208c464c078ec.




