import boto3,json


def refresh():
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

refresh()
