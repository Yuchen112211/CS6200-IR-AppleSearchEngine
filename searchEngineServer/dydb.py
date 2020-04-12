import boto3,json

from boto3.dynamodb.conditions import Key, Attr

class db(object):

	def __init__(self):
		dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
		client = boto3.client('dynamodb', region_name='us-east-2')
		self.table = dynamodb.Table('apple')
		self.table_item = dynamodb.Table('apple-tokens')

		file = open("token_storage.txt", "r")
		tokens_raw = file.readlines()
		tokens_dict = [json.loads(i) for i in tokens_raw]

		self.token = {}

		for i in range(len(tokens_dict)):
			token_item = tokens_dict[i]['tokens']
			raw_token = token_item.split(",")
			final_token = {}
			for k in raw_token:
				temp = k.split(':')
				if len(temp) != 2:
					continue
				else:
					token, freq = temp
					final_token[token] = int(freq)
			self.token[tokens_dict[i]['id']] = final_token


	def fetch_genre(self, genre, max_length):
		rst = []
		f = open('data_genre/data_%s.txt' % genre,'r')
		data = f.readlines()
		rst = [json.loads(i) for i in data]
		final = []
		for d in range(min(len(rst),max_length)):
			i = rst[d]
			if 'rating' in i:
				i['frate'] = float(i['rating'])
			else:
				i['frate'] = float(i['user_rating'])
			final.append(i)
		rst = sorted(final, key=lambda x:-x['frate'])
		print "Read genre: " + genre
		
		return rst

	def fetch_all(self, max_length):
		rst = []
		f = open('app_storage.txt','r')
		data = f.readlines()
		rst = [json.loads(i) for i in data]
		final = []
		for d in range(min(len(rst),max_length)):
			i = rst[d]
			if 'rating' in i:
				i['frate'] = float(i['rating'])
			else:
				i['frate'] = float(i['user_rating'])
			final.append(i)
		rst = sorted(final, key=lambda x:-x['frate'])
		print "Read all"

		return rst

	def fetch_token_by_id(self, uid):
		if uid in self.token:
			return self.token[uid]

	def fetch_item_by_name(self, name):
		response = self.table.query(
			KeyConditionExpression=Key('name').eq(name),
			)
		if response['Items']:
			return response['Items'][0]

