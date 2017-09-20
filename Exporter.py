# -*- coding: utf-8 -*-
import sys,getopt,datetime,codecs
import re


if sys.version_info[0] < 3:
    import got
else:
    import got3 as got
    

def cleanText(text):

	text = text.replace(","," ").replace("\n", " ").replace("\r", " ").replace("\r\n", " ")
	filtered_text = ""
    
	words = text.split(" ")
	for i in range(0,len(words)):
		words[i] = words[i].strip().lower()
        
		try:
			if words[i].startswith('http'):
				words[i] = ""
		except:
			pass

	text = " ".join(words)
	
	filtered_text = text
    
    #keep only informative characters
	#filtered_text = re.sub('[^a-z|A-Z|0-9|\s|\.|@]', '', text);
    
	return filtered_text	

def main(argv):

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return

	if len(argv) == 1 and argv[0] == '-h':
		f = open('exporter_help_text.txt', 'r')
		print f.read()
		f.close()

		return

	try:
		opts, args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output="))

		tweetCriteria = got.manager.TweetCriteria()
		outputFileName = "output_got.csv"

		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg

			elif opt == '--since':
				tweetCriteria.since = arg

			elif opt == '--until':
				tweetCriteria.until = arg

			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg

			elif opt == '--toptweets':
				tweetCriteria.topTweets = True

			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)
			
			elif opt == '--near':
				tweetCriteria.near = '"' + arg + '"'
			
			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--output':
				outputFileName = arg
				
		outputFile = codecs.open(outputFileName, "a", "utf-8")

		#outputFile.write('username,date,retweets,favorites,text,geo,mentions,hashtags,id,permalink')

		print('Searching...\n')

		def receiveBuffer(tweets):
			
			for t in tweets:
				outputFile.write(('\n%s,%s,%d,%d,%s,%s,%s,%s,%s' % (t.username, str(t.date.strftime("%Y-%m-%d")), int(t.retweets), int(t.favorites), cleanText(t.text), str(t.geo), str(t.mentions), str(t.hashtags), str("id"+t.id))))
			outputFile.flush();
			print('More %d saved on file...\n' % len(tweets))

		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

	except arg:
		print('Arguments parser error, try -h' + arg)
	finally:
		outputFile.close()
		print('Done. Output file generated "%s".' % outputFileName)

if __name__ == '__main__':
	main(sys.argv[1:])
