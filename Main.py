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

def main():

	def printTweet(descr, t):
		print(descr)
		print("Username: %s" % t.username)
		print("Retweets: %d" % t.retweets)
		print("Text: %s" % t.text)
		print("Mentions: %s" % t.mentions)
		print("Hashtags: %s\n" % t.hashtags)
	
	
	outputFileName = "output_got.csv"				
	outputFile = codecs.open(outputFileName, "a", "utf-8")
	dateSince_str = "2016-09-14"
	dateUntil_str = "2017-09-16"
	dateFinal_str = dateUntil_str
	
	#outputFile.write('username,date,retweets,favorites,text,geo,mentions,hashtags,id,permalink')

	print('Searching...\n')
	def receiveBuffer(tweets):
			
		for t in tweets:
			outputFile.write(('\n%s,%s,%d,%d,%s,%s,%s,%s,%s' % (t.username,t.date.strftime("%Y-%m-%d"), int(t.retweets), int(t.favorites), cleanText(t.text), str(t.geo), str(t.mentions), str(t.hashtags), str("id"+t.id))))
		outputFile.flush();
		print('More %d saved on file...\n' % len(tweets))
		
	
	dateFinal = datetime.datetime.strptime(dateFinal_str, "%Y-%m-%d")
	dateSince = datetime.datetime.strptime(dateSince_str, "%Y-%m-%d")

	while dateFinal>dateSince:
		tweetCriteria = got.manager.TweetCriteria().setQuerySearch('acetaminophen OR analgesics OR antipyretic OR duragesic OR durogesic OR fentanyl OR heroin OR hydrocodine OR hydrocodone OR hydromorphone OR hydros OR ibuprofen OR lortab OR methadone OR morphine OR narcotic OR narcotics OR opiate OR opioid OR opium OR oxycodone OR oxycontin OR oxycottin OR oxycotton OR percodan OR tylenol OR vicodin OR vicoprofen OR xanax').setSince(dateSince_str).setUntil(dateFinal_str)
		#tweetCriteria = got.manager.TweetCriteria().setQuerySearch('fentanyl').setSince(dateSince_str).setUntil(dateFinal_str)
		tweets = got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
		print('Switching...\n')
		dateFinal_str = tweets[-1].date.strftime("%Y-%m-%d")
		dateFinal = datetime.datetime.strptime(dateFinal_str, "%Y-%m-%d")


if __name__ == '__main__':
	main()
