import parser, dydb

import BaseHTTPServer
from io import BytesIO

database = dydb.db()
print "Setting OK."
class Handler( BaseHTTPServer.BaseHTTPRequestHandler ):

	def process(self, query, rank_order, genre):
		query_token = parser.parseQuery(query)
		complete_data =[]

		max_length = float("inf")
		#max_length = 1000
		if genre != "None":
			complete_data = database.fetch_genre(genre, max_length)
		else:
			complete_data = database.fetch_all(max_length)

		doc_cnt = len(complete_data)
		complete_token = []

		name_id = {}


		for i in range(doc_cnt):
			item = complete_data[i]
			uid = ""
			if 'uid' in item:
				uid = item['uid']
			else:
				uid = item['id']
			name_id[uid] = item['name']
			token_item = database.fetch_token_by_id(uid)

			if token_item:
				complete_token.append((uid, token_item))

		doc_cnt = min(doc_cnt, len(complete_token))
		wordAppear = parser.getWordAppear(complete_token, query_token)

		total_scores = []

		query_vector = parser.compute_query(query_token, doc_cnt, wordAppear)

		for i in range(doc_cnt):
			uid, token = complete_token[i]
			current_score = parser.get_score(token, query_token, doc_cnt, wordAppear, query_vector)
			if current_score != 0:
				total_scores.append((uid,current_score))
		showing_length = 200

		total_scores = sorted(total_scores, key=lambda x:x[1])
		showing_length = min(len(total_scores), showing_length)
		final_data = []
		for uid, score in total_scores[:showing_length]:
			cname = name_id[uid]
			current_item = database.fetch_item_by_name(cname)
			if current_item:
				if 'user_rating' in current_item:
					if current_item['user_rating'] >= rank_order and current_item['user_rating'] <= str(float(rank_order) + 1):
						final_data.append(current_item)
					else:
						continue
				else:
					if current_item['rating'] >= rank_order and current_item['rating'] <= str(float(rank_order) + 1):
						final_data.append(current_item)
					else:
						continue

		return final_data


	def prettify(self, item):
		self.wfile.write("<div>")
		self.wfile.write("<h2>")
		self.wfile.write(item['name'].encode('utf-8'))
		self.wfile.write("</h2>")
		cid = ""
		if "id" in item:
			cid = item['id']
		else:
			cid = item['uid']

		if 'rating' in item:
			self.wfile.write("<li>Rating: "+ item['rating'] +"</li>")
		else:
			self.wfile.write("<li>Rating: "+ item['user_rating'] +"</li>")

		if 'url' in item:
			self.wfile.write("<li> <a href=\"" + item['url'] + "\">App's link</a> </li>") 
		else:
			self.wfile.write("<li> <a href=\"https://apps.apple.com/us/app/id" + cid + "\">App's link</a> </li>")
		self.wfile.write("<li>description: "+ item['description'].encode('utf-8') +"</li>")
		


		self.wfile.write("</div>")

	def do_GET( self ):
		self.send_response(200)
		self.send_header( 'Content-type', 'text/html' )
		self.end_headers()
		self.wfile.write( open('indexRank.html', 'r').read() )
		self.wfile.write('</body></html')

	def do_POST( self ):

		self.send_response(200)
		self.send_header( 'Content-type', 'text/html' )
		content_length = int(self.headers.getheader('Content-Length'))

		body = self.rfile.read(content_length).split('\r\n')
		self.end_headers()

		query = body[3]
		rank_order = body[7]
		genre = body[-3]

		print_data = self.process(query, rank_order, genre)

		for i in print_data:
			self.prettify(i)




httpd = BaseHTTPServer.HTTPServer( ('127.0.0.1', 8000), Handler )
httpd.serve_forever()