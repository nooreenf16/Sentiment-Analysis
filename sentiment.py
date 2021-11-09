########   SENTIMENT ANALYSIS   #############

#libraries to create and work on data frames
import pandas as pd
import numpy as np
import re  
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
#%matplotlib inline
#libraries to scrape data from twitter
import tweepy
import webbrowser
#language processing libraries
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from spellchecker import SpellChecker
from textblob import TextBlob

consumer_key = 'D2ODhkO8XelW1GMADfgJd9xzv'
consumer_secret = 'BGuYPX18vVOkug9A3OLMo7JQhWVeWsISPfuhq9EhIbW23g3Rll'
callback_uri = 'oob'

#to authorize as a valid user
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
redirect_url = auth.get_authorization_url()
webbrowser.open(redirect_url)
user_pin = input("Pin: ")
auth.get_access_token(user_pin)
api = tweepy.API(auth)

#loading the timelines
import datetime as dt
start = dt.datetime(2020,10,10)
end = dt.datetime(2020,10,11)
t1 = api.user_timeline(screen_name = 'ndtv', tweet_mode = "extended", count= 500, lang = "en")
t2 = api.user_timeline(screen_name = 'timesofindia', tweet_mode = "extended", count= 500, lang = "en")
t3 = api.user_timeline(screen_name = 'IndiaToday', tweet_mode = "extended", count= 500, lang = "en")

#retrieving the tweets from respective timelines
texts1 = [status1.full_text for status1 in t1]
texts2 = [status2.full_text for status2 in t2]
texts3 = [status3.full_text for status3 in t3]

#creating dataframe
df1 = pd.DataFrame(texts1, columns = ['text'])
df2 = pd.DataFrame(texts2, columns = ['text'])
df3 = pd.DataFrame(texts3, columns = ['text'])

clean_text=[]
for i in df1['text']:
    message = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", i)
    message = re.sub(r"[,@\'?\:.$%_]", "",message)
    message = re.sub('[^a-zA-Z/:.\d]',' ',message)
    message = re.sub(r"\s+"," ", message)
    message = message.lower()
    message = message.split()
    ps = PorterStemmer()
    all_words = stopwords.words('english')
    message = [ps.stem(word) for word in message if not word in set(all_words)]
    message = ' '.join(message)
    clean_text.append(message)
df1['text']= clean_text

clean_text = []
for i in df2['text']:
    message = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", i)
    message = re.sub(r"[,@\'?\:.$%_]", "",message)
    message = re.sub('[^a-zA-Z/:.\d]',' ',message)
    message = re.sub(r"\s+"," ", message)
    message = message.lower()
    message = message.split()
    ps = PorterStemmer()
    all_words = stopwords.words('english')
    message = [ps.stem(word) for word in message if not word in set(all_words)]
    message = ' '.join(message)
    clean_text.append(message)
df2['text']= clean_text

clean_text = []
for i in df3['text']:
    message = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", i)
    message = re.sub(r"[,@\'?\:.$%_]", "",message)
    message = re.sub('[^a-zA-Z/:.\d]',' ',message)
    message = re.sub(r"\s+"," ", message)
    message = message.lower()
    message = message.split()
    ps = PorterStemmer()
    all_words = stopwords.words('english')
    message = [ps.stem(word) for word in message if not word in set(all_words)]
    message = ' '.join(message)
    clean_text.append(message)
df3['text']= clean_text

pol1, pol2, pol3 = [], [], []
for i in range(len(df1)):
    pol1.append(TextBlob(df1['text'][i]).sentiment.polarity)
    pol2.append(TextBlob(df2['text'][i]).sentiment.polarity)
    pol3.append(TextBlob(df3['text'][i]).sentiment.polarity)
    
df1["Polarity"] = pol1
df2["Polarity"] = pol2
df3["Polarity"] = pol3

senti1, senti2, senti3 = [], [], []

for i in range(len(df1['Polarity'])):
    if df1['Polarity'][i]>0: senti1.append('Positive')
    elif df1['Polarity'][i]<0: senti1.append('Negative')
    else: senti1.append('Neutral')
        
for i in range(len(df1['Polarity'])):
    if df2['Polarity'][i]>0: senti2.append('Positive')
    elif df2['Polarity'][i]<0: senti2.append('Negative')
    else: senti2.append('Neutral')
        
for i in range(len(df1['Polarity'])):
    if df3['Polarity'][i]>0: senti3.append('Positive')
    elif df3['Polarity'][i]<0: senti3.append('Negative')
    else: senti3.append('Neutral')
        
df1["Sentiment"] = senti1
df2["Sentiment"] = senti2
df3["Sentiment"] = senti3

#getting the number of positve and negative tweets
ptext1 = sum([1 for i in range(len(df1)) if df1['Sentiment'][i]=='Positive'])
ptext2 = sum([1 for i in range(len(df2)) if df2['Sentiment'][i]=='Positive'])
ptext3 = sum([1 for i in range(len(df3)) if df3['Sentiment'][i]=='Positive'])

ntext1 = sum([1 for i in range(len(df1)) if df1['Sentiment'][i]=='Negative'])
ntext2 = sum([1 for i in range(len(df2)) if df2['Sentiment'][i]=='Negative'])
ntext3 = sum([1 for i in range(len(df3)) if df3['Sentiment'][i]=='Negative'])

#getting the positive and negative tweets percentage
panalysis1 = round(ptext1 / len(df1) *100)
panalysis2 = round(ptext2 / len(df2) *100)
panalysis3 = round(ptext3 / len(df3) *100)

nanalysis1 = round(ntext1 / len(df1) *100)
nanalysis2 = round(ntext2 / len(df2) *100)
nanalysis3 = round(ntext3 / len(df3) *100)

#plotting graphs for tweets percentage
y = [panalysis1, panalysis2, panalysis3]
x = ["NDTV", "AAJTAK", "INDIATODAY"]
plt.bar(x,y)

y = [nanalysis1, nanalysis2, nanalysis3]
x = ["NDTV", "AAJTAK", "INDIATODAY"]
plt.bar(x,y)

#plotting graphs for negative tweets percentage
y = [nanalysis1, nanalysis2, nanalysis3]
x = ["NDTV", "AAJTAK", "INDIATODAY"]
plt.bar(x,y)