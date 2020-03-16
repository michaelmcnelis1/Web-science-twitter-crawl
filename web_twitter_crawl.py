
import json
import csv
import tweepy #pip
import re
import nltk
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
#nltk.download('vader_lexicon')
#sid = SentimentIntensityAnalyzer()
#import unicodedata
import emoji #pip
from autocorrect import Speller #pip
auto_correct=Speller(lang="en")
import pandas as pd
import regex #pip

#function to count the number of emojis in a tweet 
def emoji_count(text):
    emoji_count = 0
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_count = emoji_count + 1
            text = text.replace(word, '') 
    return emoji_count
#######
 #open the file to include all the data   
with open("abc.csv", 'a',encoding='utf-8-sig') as file:

        w = csv.writer(file)###
        w.writerow(['tweet_id','timestamp','Tweet_text'])

######


#create a function to search for specific hashtags
def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase,fname):
    
    #create authentication for accessing Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy API
    api = tweepy.API(auth,wait_on_rate_limit=True)
    #open the spreadsheet we will write to
    with open('%s.csv' % (fname), 'a',encoding='utf-8-sig') as file:

        w = csv.writer(file)###
        for tweet in tweepy.Cursor(api.search, q=hashtag_phrase+' -filter:retweets AND -filter:replies AND -filter:quotes AND -filter:links AND -filter:mentions', 
                                   lang="en", tweet_mode='extended').items(1500):
            #filter so at most 3 hastags - keep tweets clean and avoid ambiguity between categories
            hashtags = 0
            mentions = 0
            for i in tweet.full_text:
                if i == "#":
                    hashtags = hashtags +1

            if hashtags <=3 and mentions <=1 and emoji_count(str(tweet.full_text.replace('\n',' '))) <=3:
                w.writerow([tweet.id,tweet.created_at,str(tweet.full_text.replace('\n',' '))]) 

#create a function to search for specific emojis -  basically same as above
def search_for_emojis(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase,fname):
    
    #create authentication for accessing Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy API
    #added wait_on_rate_limit=True myself - if it breaks then remove it
    api = tweepy.API(auth,wait_on_rate_limit=True)

    #open the spreadsheet we will write to
    with open('%s.csv' % (fname), 'a',encoding='utf-8-sig') as file: #must be encoded utf-8-sig for emojis 

        w = csv.writer(file)###
        for tweet in tweepy.Cursor(api.search, q=hashtag_phrase+' -filter:retweets AND -filter:replies AND -filter:quotes AND -filter:links AND -filter:mentions', 
                                   lang="en", tweet_mode='extended').items(1500):
            #filters so there are at most 3 hashtags and at most 3 emojis
            hashtags = 0
            mentions = 0
            for i in tweet.full_text:
                if i == "#":
                    hashtags = hashtags +1
            if hashtags <=3 and mentions <=1 and emoji_count(str(tweet.full_text.replace('\n',' '))) <=3:
                    w.writerow([tweet.id,tweet.created_at,str(tweet.full_text.replace('\n',' '))]) 

consumer_key = "1jpVeTwvYNN9Ahvw7vxMGJyJH"
consumer_secret = "mbXU9HXWhpc8UPpBdTWSgQjy5918qvr0Hhq6vkMOUmqTau0C8W"
access_token = "1223915353132208128-motQaOUhZZ98ssJfmIAV3slNvRHhav"
access_token_secret = "IYWefwREPeuI7pwoiuMpa9coAbVvXCUWlGDeJgrtDdJzr"

   
#create a list of keywords, and words to omit, for each emotion
hashtag_phrase = [#happy
                    "#happy OR #happiness AND -surprise AND -shock AND -angry AND -anger AND -fear AND -scared AND -quote AND -enjoyable AND -pleasant AND -excitement AND -excited AND -sad",
                  #angry
                  "#angry AND -#happy AND -happiness AND -surprise AND -shock AND -fear AND -scared AND -quote AND -enjoyable AND -pleasant AND -excitement AND -excited AND -sad",
                  #fear
                  "#scare OR #scared OR #afraid OR #fear OR #anxious OR #panic AND -happy AND -happiness AND -surprise AND -shock AND -angry AND -anger AND -quote AND -enjoyable AND -pleasant AND -#excitement AND -excited AND -sad",
                  #sad
                  "#sad OR #sadness AND -surprise AND -shock AND -angry AND -anger AND -fear AND -scared AND -quote AND -enjoyable AND -pleasant AND -excitement AND -excited AND -panic",
                  #pleasant
                  "#enjoyable OR #pleasant OR #lovely OR #delightful AND -happy AND -happiness AND -surprise AND -shock AND -angry AND -anger AND -fear AND -scared AND -#quote AND -excitement AND -excited AND -sad",
                  #excited
                  "#excitement OR #excited AND -happy AND -happiness AND -surprise AND -shock AND -angry AND -anger AND -fear AND -scared AND -#quote AND -enjoyable AND -pleasant AND -sad"]
                  
#create a list of emojis, and emojis and words to omit, for each emotion
emoji_list = [#happy
                "😊 AND -sad  AND -🍑 AND -excited AND -1) AND -💦 AND -👿 AND -😮 AND -😌 AND -🤩 AND -😱 AND -🔥 AND -surprise AND -shock AND -angry AND -anger AND -fear AND -scared AND -quote AND -enjoyable AND -pleasant AND -excitement AND -excited AND -sad AND -lovely AND -delightful",
                #angry
                "😠 AND -🍑 AND -😊  AND -1) AND -💦 AND -👺 AND -❤️ AND -😍 AND -😮 AND -😌 AND -🤩 AND -😱 AND -🔥 AND -😇 -happy AND -happiness AND -surprise AND -shock AND -fear AND -scared AND -quote AND -enjoyable AND -pleasant AND -excitement AND -excited AND -sad AND -lovely AND -delightful",
                #fear
                "😱 AND -😇 AND -😊  AND -🍑 AND -1) AND -💦 AND -❤️ AND -👿 AND -😍 AND -😮 AND -😌 AND -🤩 AND -🔥 AND -😇 AND -happy AND -happiness AND -surprise AND -shock AND -angry AND -anger AND -quote AND -enjoyable AND -pleasant AND -#excitement AND -excited AND -sad AND -lovely AND -delightful",               
                #sad
                "😢 AND -😄 AND -😊 AND -🍑 AND -enjoyable AND -pleasant AND -lovely AND -delightful AND -1) AND -💦 AND -❤️ AND -👿 AND -😍 AND -😮 AND -🤩 AND -😱  AND -🔥 AND -happy AND -happiness AND -surprise AND -shock AND -angry AND -anger AND -fear AND -scared AND -#quote AND -excitement AND -excited",
                #pleasant
                "😄 AND -🍑 AND -😊 AND -1) AND -💦 AND -❤️ AND -👿 AND -😍 AND -😮 AND -🤩 AND -😱  AND -🔥 AND -happy AND -happiness AND -surprise AND -shock AND -angry AND -anger AND -fear AND -scared AND -#quote AND -excitement AND -excited AND -sad",
                #excited
                "🤩 AND -🍑 AND -😊 AND -1) AND -💦 AND -❤️ AND -👿 AND -😍 AND -😮 AND -😌 AND -😱  AND -🔥 AND -happy AND -happiness AND -surprise AND -shock AND -angry AND -anger AND -fear AND -scared AND -#quote AND -enjoyable AND -pleasant AND -sad AND -lovely AND -delightful"]





#add tweets with the hashtags into a file containing all the data
for i in range(0,(len(hashtag_phrase))):
    if __name__ == '__main__':
        search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase[i],fname="abc")

#add tweets with the emojis into a file containing all the data
for i in range(0,(len(emoji_list))):
    if __name__ == '__main__':
        search_for_emojis(consumer_key, consumer_secret, access_token, access_token_secret, emoji_list[i],fname="abc")



   

 


     
        
        
   
        
        
        
        
        
        
    