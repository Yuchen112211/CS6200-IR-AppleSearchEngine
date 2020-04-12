# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import boto3

from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize
from collections import Counter

class AppleapplicationPipeline(object):

	def open_spider(self, spider):
		dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
		self.table = dynamodb.Table("apple")
		self.table_token = dynamodb.Table("apple-tokens")
		stoplist = ' '.join(open('stoplist.txt', 'r').readlines())
		self.stop_words = set(stoplist.split())
		self.ps = PorterStemmer()

	def process_item(self, item, spider):
		res = self.table.put_item (Item = dict(item))

		sentence = (item['description'] + item['name']).strip()
		tokens = word_tokenize(sentence)
		tokens = [self.ps.stem(token) for token in tokens]
		token_cnt = Counter(tokens)
		final_token = ''
		for token in token_cnt:
			if token in self.stop_words:
				continue
			else:
				final_token += (token)
				final_token += ":"
				final_token += str(token_cnt[token])
				final_token += ","
		token_item = {'id':item['uid'], 'tokens':final_token}

		res1 = self.table_token.put_item(Item = dict(token_item))
		return item
