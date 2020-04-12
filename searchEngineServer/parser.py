from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize
from collections import Counter, defaultdict
import math
ps = PorterStemmer()
stoplist = ' '.join(open('/Users/macbookair11/Desktop/github-repo/CS6200-IR-AppleSearchEngine/app-store-apple-data-set-10k-apps/stoplist.txt', 'r').readlines())
stop_words = set([ps.stem(i) for i in stoplist.split()])

def parseQuery(query):
	tokens = word_tokenize(query)
	tokens = [ps.stem(token) for token in tokens]
	token_cnt = Counter(tokens)
	final_token = {}
	for token in token_cnt:
		if token in stop_words:
			continue
		final_token[token] = int(token_cnt[token])
	return final_token

def getWordAppear(complete_token, query_token):
	appearance = defaultdict(int)
	for uid, token in complete_token:
		for term in query_token:
			if term in token:
				appearance[term] += 1
	return appearance

def compute_query(query_token, doc_cnt, appearance):
	N = doc_cnt
	word_number = 0
	for token in query_token:
		word_number += query_token[token]
	query_vector = []
	for term in query_token:
		tf = float(query_token[term]) / float(word_number)
		df = appearance[term]
		if df == 0 or df == N:
			query_vector.append(0)
			continue
		score = math.log(1 + float(tf)) / math.log(float(N) / float(df), 10)
		query_vector.append(score*100)
	return query_vector

def compute_cosine(vector1, vector2):
	top = sum([vector1[i] * vector2[i] for i in range(len(vector1))])
	bottom = math.sqrt(sum([pow(i,2) for i in vector1]))
	return float(top) / float(bottom) + (len(vector2) - vector2.count(0)) * 2 if bottom > 0 else 0

def get_score(token_item, query_token, doc_cnt, appearance, query_vector):
	N = doc_cnt
	word_number = 0
	for token in token_item:
		word_number += token_item[token]

	token_vector = []
	for term in query_token:
		if term not in token_item:
			token_vector.append(0)
			continue

		tf = float(token_item[term]) / float(word_number)
		df = appearance[term]
		if df == 0 or df == N:
			token_vector.append(0)
			continue
		score = math.log(1 + float(tf)) / math.log(float(N) / float(df), 10)
		token_vector.append(score*100)

	current_score = compute_cosine(token_vector, query_vector)
	return current_score


