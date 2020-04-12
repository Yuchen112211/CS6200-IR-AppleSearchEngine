import boto3,json
from boto3.dynamodb.conditions import Key, Attr

def refresh_genre():
	dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
	table = dynamodb.Table("apple")
	genres = ['Productivity', 'Photo & Video', 'Entertainment', 'Travel','Sports',
	'Food & Drink', 'Book', 'Music', 'Shopping', 'Finance', 'Business', 'Navigation',
	'Utilities', 'News', 'Lifestyle', 'Medical', 'Games', 'Catalogs', 'Health & Fitness',
	'Social Networking', 'Reference', 'Weather', 'Education', 'Stickers']

	for genre in genres:
		second_genre = genre.lower().replace(" & ","-")
		second_genre = 'ios-' + second_genre
		if genre =='Book':
			second_genre += 's'
		rst = []
		response = table.scan(
			FilterExpression=Attr("prime_genre").eq(genre),
			ProjectionExpression="#n, id,uid,rating,user_rating",
			ExpressionAttributeNames={"#n":"name"}
			)
		rst += response['Items']
		while response['Count'] > 0 and 'LastEvaluatedKey' in response:
			LastKey = response['LastEvaluatedKey']
			response = table.scan(
				FilterExpression=Attr("prime_genre").eq(genre),
				ProjectionExpression="#n, id,uid,rating,user_rating",
				ExclusiveStartKey=LastKey,
				ExpressionAttributeNames={"#n":"name"}
				)
			rst += response['Items']

		response = table.scan(
			FilterExpression=Attr("classification").eq(second_genre),
			ProjectionExpression="#n, id,uid,rating,user_rating",
			ExpressionAttributeNames={"#n":"name"}
			)
		rst += response['Items']
		while response['Count'] > 0 and 'LastEvaluatedKey' in response:
			LastKey = response['LastEvaluatedKey']
			response = table.scan(
				FilterExpression=Attr("classification").eq(second_genre),
				ProjectionExpression="#n, id,uid,rating,user_rating",
				ExclusiveStartKey=LastKey,
				ExpressionAttributeNames={"#n":"name"}
				)
			rst += response['Items']
		total_tokens = [json.dumps(item) for item in rst]
		string = "\n".join(total_tokens)
		file = open("data_genre/data_%s.txt" % genre,"wr")
		file.write(string)
		file.close()


def refresh_tk():
	dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
	table = dynamodb.Table("apple-tokens")

	response = table.scan()

	rst = []
	rst += response['Items']

	while response['Count'] > 0 and 'LastEvaluatedKey' in response:
		response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
		rst += response['Items']

	total_tokens = [json.dumps(item) for item in rst]
	string = "\n".join(total_tokens)
	file = open("token_storage.txt","wr")
	file.write(string)
	file.close()

def refresh():
	dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
	table = dynamodb.Table("apple")

	response = table.scan(
		ProjectionExpression="#n, id,uid,rating,user_rating",
		ExpressionAttributeNames={"#n":"name"}
		)

	rst = []
	rst += response['Items']

	while response['Count'] > 0 and 'LastEvaluatedKey' in response:
		response = table.scan(
			ProjectionExpression="#n, id, uid, rating, user_rating",
			ExpressionAttributeNames={"#n":"name"},
			ExclusiveStartKey=response['LastEvaluatedKey']
			)
		rst += response['Items']

	total_tokens = [json.dumps(item) for item in rst]
	string = "\n".join(total_tokens)
	file = open("app_storage.txt","wr")
	file.write(string)
	file.close()

refresh()
print "General finished."
refresh_tk()
print "Tokens finished."
refresh_genre()
print "Genres finished."

