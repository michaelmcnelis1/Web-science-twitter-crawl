# -*- coding: utf-8 -*-

#import time
#import json
import csv
#import tweepy #pip
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()# to examine the strength of the sentiment expressed in a tweet
import unicodedata
import emoji #pip
from autocorrect import Speller #pip
auto_correct=Speller(lang="en")# an autocorrect function
import pandas as pd
import regex #pip
import numpy as np
import random
import os

#create a function to remove contractions and other gramatical annomalies
def decontracted(phrase):
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"can\’t", "can not", phrase)
    phrase = re.sub(r"i\'m", "I am", phrase)
    phrase = re.sub(r"&amp", " ", phrase) 
    phrase = re.sub(r" ; ", " and ", phrase)
    phrase = re.sub(r"how\'d", "how did", phrase)
    phrase = re.sub(r"i\'d", "I would", phrase)
    phrase = re.sub(r"he\'d", "he had", phrase)
    phrase = re.sub(r"ain\'t", "are not", phrase)
    phrase = re.sub(r"you\'d", "you had", phrase)
    phrase = re.sub(r"ain\’t", "are not", phrase)
    phrase = re.sub(r"he\'s", "he is", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
     #general cases with a different apostrophe to above
    phrase = re.sub(r"’re", " are", phrase)
    phrase = re.sub(r"’d", " would", phrase)
    phrase = re.sub(r"’ll", " will", phrase)
    phrase = re.sub(r"n’t", " not", phrase)
    phrase = re.sub(r"’ve", " have", phrase)
    phrase = re.sub(r"’m", " am", phrase)
    #abbreviations
    phrase = re.sub(r"yolo", "you only live once", phrase)
    phrase = re.sub(r"tbt", "throwback Thusrday", phrase)
    phrase = re.sub(r"idk", "I don't know", phrase)
    phrase = re.sub(r" imo ", "in my opinion", phrase)
    phrase = re.sub(r" omw ", "on my way", phrase)
    phrase = re.sub(r"tbf", "to be fair", phrase)
    phrase = re.sub(r"tbh", "to be honest", phrase)
    phrase = re.sub(r" btw", " by the way", phrase)
    phrase = re.sub(r"fb", "Facebook", phrase)
    phrase = re.sub(r"ftw", "for the win", phrase)
    phrase = re.sub(r" ig ", " instagram ", phrase)
    phrase = re.sub(r"omg", "oh my god", phrase)
    phrase = re.sub(r"lol", "laughing out loud", phrase)
    phrase = re.sub(r"jk", "just kidding", phrase)
    phrase = re.sub(r" smh ", "shaking my head", phrase)
    phrase = re.sub(r"y’all", "you all", phrase)
    phrase = re.sub(r"y'all", "you all", phrase)
    phrase = re.sub(r"bc", "because", phrase)
    phrase = re.sub(r"pls", "please", phrase)
    phrase = re.sub(r"tnx", "thanks", phrase)
    phrase = re.sub(r"abt", "about", phrase)
    phrase = re.sub(r"wanna", "want to", phrase)
    phrase = re.sub(r"tv", "television", phrase)
    phrase = re.sub(r"dnt", "do not", phrase)
    phrase = re.sub(r"(.)\1+",r"\1\1",phrase) #takes repeated letters and replaces them with double letters, 
                                                #eg. happppy goes to happy
    phrase = re.sub(r" rn ",r" right now ",phrase)
    phrase = re.sub(r" rly",r" really",phrase)
    phrase = re.sub(r" mins ",r" minutes ",phrase)
    phrase = re.sub(r"gonna",r"going to",phrase)
    phrase = re.sub(r"imma",r"I am going to",phrase)
    phrase = re.sub(r"luv",r"love",phrase)
    phrase = re.sub(r"wtf",r"what",phrase)
    phrase = re.sub(r"fkn",r" ",phrase)
    phrase = re.sub(r" rn,",r" right now,",phrase)
    phrase = re.sub(r"&gt;",r"greater than",phrase)
    phrase = re.sub(r"&lt;",r"less than",phrase)
    phrase = re.sub(r"&ge;",r"greater than or equal to",phrase)
    phrase = re.sub(r"&le;",r"less than or equal to",phrase)
    phrase = re.sub(r"dawg",r"dog",phrase)
    phrase = re.sub(r" gm ",r" good morning ",phrase)
    phrase = re.sub(r" u ",r" you ",phrase)
    phrase = re.sub(r"b4",r"before",phrase)
    phrase = re.sub(r" tm ",r" tomorrow ",phrase)
    phrase = re.sub(r"fml",r"freak my life",phrase)
    phrase = re.sub(r"lmao",r"laughing out loud",phrase)
    phrase = re.sub(r"lmfao",r"laughing out loud",phrase)
    phrase = re.sub(r"congrats",r"congratulations",phrase)
    phrase = re.sub(r" ima ",r" I am going to ",phrase)
    phrase = re.sub(r"yr", "year", phrase)
    phrase = re.sub(r"cuda",r"could have",phrase)
    phrase = re.sub(r"cudda",r"could have",phrase)
    phrase = re.sub(r"gotta",r"got to",phrase)
    phrase = re.sub(r"wanna",r"want to",phrase)
    phrase = re.sub(r'[\?\.\!]+(?=[\?\.\!])', '', phrase) #replaces repeated ? or ! or . charcters with the last one in the string
                                                            #eg. ?!!!!!!?!?..! becomes !
    phrase = re.sub(r"loml",r"love of my life",phrase)
    phrase = re.sub(r" bout ",r" about ",phrase)
    phrase = re.sub(r"w/",r"with",phrase)

    return phrase

#create a function to remove duplicates
def remove_duplicates(filename):  
    data = pd.read_csv('%s.csv' % (filename))
    data.drop_duplicates(subset="tweet_text",keep=False,inplace=True)        
    data.to_csv('%s25.csv' % (filename),encoding ="utf-8-sig")


#read the file containing all the data into a dataframe
df = pd.read_csv("all_data.csv")

#create a function to count the number of emojis 
def emoji_count(text):
    emoji_count = 0
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_count = emoji_count + 1
            text = text.replace(word, '') 
    return emoji_count

#create a list of file names
fname = ["happy_tweets","pleasant_tweets","excitement_tweets","angry_tweets","fear_tweets","sad_tweets"]

#create the list of lists of keywords/emojis pertaining to each emotion
phrases= [["#happy","#happiness","😊"],
           ["#enjoyable","#pleasant","#lovely","#delightful","😄"],
            ["#excitement","#excited","🤩"],
           ["angry","#angry",'😠' ],
            ["#scare","#scared","#scared","#afraid", "😱","afraid","#fear","#anxious","#panic"],
            ["#sad","#sadness"]]

#create a function to clean and add tweets to given csv file for positive emotions             
def clean_data_positive(fname,phrases):          
    with open('%s.csv' % (fname), 'w+',encoding='utf-8-sig') as outfile:
        w = csv.writer(outfile)
        w.writerow(['tweet_id','timestamp','tweet_text'])
        for i in range(0,len(df)):
            if df["Tweet_text"][i].lower().split()[(len(df["Tweet_text"][i].split())-1)] in phrases:#checks that the last word is a hashtag pertaining to the emotion
                if any(s in df["Tweet_text"][i].lower() for s in phrases):
                    no_words=len(df["Tweet_text"][i].split())
                    if no_words >=4:
                        if sid.polarity_scores(df["Tweet_text"][i])["compound"] >=.45: #ensures the sentiment is strong enough to be included
                            if emoji_count(df["Tweet_text"][i]) <=3:
                                w.writerow([df["tweet_id"][i],df["timestamp"][i],auto_correct(decontracted(str(df["Tweet_text"][i]).lower()))])
            if df["Tweet_text"][i].lower().split()[(len(df["Tweet_text"][i].split())-2)] in phrases and df["Tweet_text"][i].lower().split()[(len(df["Tweet_text"][i].split())-1)][0]=="#":
            #checks that the second last word is a hashtag pertaining to the emotion and the last word is a hashtag 
                if any(s in df["Tweet_text"][i].lower() for s in phrases):
                    no_words=len(df["Tweet_text"][i].split())
                    if no_words >=4:
                        if sid.polarity_scores(df["Tweet_text"][i])["compound"] >=.45: #ensures the sentiment is strong enough to be included
                           if emoji_count(df["Tweet_text"][i]) <=3: 
                                w.writerow([df["tweet_id"][i],df["timestamp"][i],auto_correct(decontracted(str(df["Tweet_text"][i]).lower()))])

#create a function to clean and add tweets to given csv file for negative emotions                     
def clean_data_negative(fname,phrases):  ###        
    with open('%s.csv' % (fname), 'w+',encoding='utf-8-sig') as outfile:#####
        w = csv.writer(outfile)###
        w.writerow(['tweet_id','timestamp','tweet_text'])
        for i in range(0,len(df)):
            if df["Tweet_text"][i].lower().split()[(len(df["Tweet_text"][i].split())-1)] in phrases: #checks that the last word is a hashtag pertaining to the emotion
                if any(s in df["Tweet_text"][i].lower() for s in phrases):
                    no_words=len(df["Tweet_text"][i].split())
                    if no_words >=4:
                        if sid.polarity_scores(df["Tweet_text"][i])["compound"] <=-.45: #ensures the sentiment is strong enough to be included
                            if emoji_count(df["Tweet_text"][i]) <=3:
                                w.writerow([df["tweet_id"][i],df["timestamp"][i],auto_correct(decontracted(str(df["Tweet_text"][i]).lower()))])
            if df["Tweet_text"][i].lower().split()[(len(df["Tweet_text"][i].split())-2)] in phrases and df["Tweet_text"][i].lower().split()[(len(df["Tweet_text"][i].split())-1)][0]=="#":
            #checks that the second last word is a hashtag pertaining to the emotion and the last word is a hashtag 
                if any(s in df["Tweet_text"][i].lower() for s in phrases):
                    no_words=len(df["Tweet_text"][i].split())
                    if no_words >=4:
                        if sid.polarity_scores(df["Tweet_text"][i])["compound"] <=-.45: #ensures the sentiment is strong enough to be included
                            if emoji_count(df["Tweet_text"][i]) <=3:
                                w.writerow([df["tweet_id"][i],df["timestamp"][i],auto_correct(decontracted(str(df["Tweet_text"][i]).lower()))])
                        


 
#add clean data for positive emotions and remove duplicates
for i in range(0,3):
    clean_data_positive(fname[i],phrases[i])
    remove_duplicates(fname[i])
    os.remove('%s.csv' % (fname[i]))
    
#add clean data for negative emotions and remove duplicates   
for i in range(3,6):
    clean_data_negative(fname[i],phrases[i])
    remove_duplicates(fname[i])
    os.remove('%s.csv' % (fname[i]))
 
#generate the random sequence of numbers to decide which tweets are used in crowdsourcing 
tweet_no=[]
for i in range(0,15):
    pos = random.randint(2,152)
    tweet_no.append(pos)        
tweet_no       
 
#shuffle a list to randomise the order in which the emotions are included in the crowdsourcing csv       
positioning= []        
for i in range(0,16):        
    tweet_pos = ["happy","pleasant","excited","sad","angry","fear"]        
    random.shuffle(tweet_pos)        
    positioning.append(tweet_pos)       
        
positioning  
