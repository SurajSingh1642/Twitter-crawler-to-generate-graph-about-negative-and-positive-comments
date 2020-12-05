
import pyttsx3
import speech_recognition as sr

import datetime

import psutil
import smtplib
import nltk
import json
import csv
import tweepy
import re
from textblob import TextBlob 
import csv
import pandas as pd 
import numpy
import matplotlib.pyplot as plt 



nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)





def speak(audio):
    engine.say(audio)
    engine.runAndWait() 




    

    
def takeCommand():

    #take microphone input and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")


    except Exception:
        print("didn't catch that")
        speak("please, say that again")
        return 'None'
    return query


if __name__ == "__main__":
    query = takeCommand().lower()
    tokens = nltk.word_tokenize(query)
    tagged = nltk.pos_tag(tokens)
    print(tagged)
hashtag_phrase=[]
for j in tagged:
    if(j[1]=='NNS' or j[1]=='NNP' or j[1]=='NNS' or j[1]=='NNPS'or j[1]=='NN'):
        hashtag_phrase.append('#'+j[0])

print(hashtag_phrase)





def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase1):
    
    #create authentication for accessing Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
        #initialize Tweepy API
    api = tweepy.API(auth)
    
    #get the name of the spreadsheet we will write to
    fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase1.decode('utf-8')))
    
    #open the spreadsheet we will write to
    with open('%s.csv' % (fname), 'w', encoding="utf-8") as file:
        
        w = csv.writer(file)
        

        #write header row to spreadsheet
        w.writerow(['timestamp', 'tweet_text', 'username','sentiment', 'all_hashtags', 'followers_count'])
        pubic_tweets=tweepy.Cursor(api.search, q=hashtag_phrase1.decode('utf-8') + ' -filter:retweets', lang="en", tweet_mode='extended').items(100)
        
        #for each tweet matching our hashtags, write relevant info to the spreadsheet
        for tweet in pubic_tweets:
            #checking polarity
            text1 =tweet.full_text
            text =' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ", text1).split())

            analysis= TextBlob(text)
            polarity = 'Positive'
            if(analysis.sentiment.polarity < 0):
                polarity = 'Negative'
            if(0<=analysis.sentiment.polarity <=0.2):
                polarity = 'Neutral'
            #WRITTING TO FILE
            w.writerow([tweet.created_at,text,
                        tweet.user.screen_name.encode('utf-8'),polarity,
                        [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])
#TWITTER KEYS
consumer_key = 'TieWMF0T7PRgeCRMK2wqpSGkc'
consumer_secret = '52cx1Gp4szYZ330HrBAod3mU32PpZdzSeGynBLaZJoxbCTFtdv'
access_token = '1015294450006757376-yPKrTjN1ay3Zlbb8fIvjoQnutYYQoy'
access_token_secret = 'TiVHn90MYwxhx8aHqHIOCUO9EbH5O0ygTvI1983vdM3Pg'

#THE ACTUAL QUERY

#DRIVER
if __name__ == '__main__':
    labels=[]
    for i in hashtag_phrase:
        search_for_hashtags(consumer_key.encode(encoding='utf-8'), consumer_secret.encode(encoding='utf-8'), access_token.encode(encoding='utf-8'), access_token_secret.encode(encoding='utf-8'), i.encode(encoding='utf-8'))
        labels.append(i)
    #Plotting piechart
    sample_data=pd.read_csv('C:\\Users\\BEAST\\Documents\\uhackathon\\'+hashtag_phrase[0].replace('#','')+".csv")
    pol1=0
    pol2=0
    pol3=0
    df = pd.DataFrame(sample_data, columns = ['sentiment'] ) 
    df=numpy.array(df)
    for i in df:
        if(i=='Neutral'):
            pol1=pol1+1
        elif(i=='Positive'):
            pol2=pol2+1
        if(i=='Negative'):
            pol3=pol3+1
    if(df.__len__()==0):
        print( "no tweets ")
    else:
        n_perc=(pol1*100)/df.__len__()
        p_perc=(pol2*100)/df.__len__()
        negative_perc=(pol3*100)/df.__len__()
        values=[n_perc,p_perc,negative_perc]
        colors=['b','g','r']
        labels.append("50-50 chances of winning")
        plt.pie(values, colors=colors, labels= values,counterclock=False, shadow=True)
        plt.title('Sentimental Analysis')
        plt.legend(labels,loc=3)
        plt.show()