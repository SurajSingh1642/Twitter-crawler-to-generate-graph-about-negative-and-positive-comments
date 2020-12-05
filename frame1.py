import pyttsx3
import speech_recognition as sr
import psutil
import pandas as pd 
import json
import csv
import tweepy
import re
from textblob import TextBlob
import pandas as pd 
import numpy
import matplotlib.pyplot as plt 
import pyaudio
import matplotlib.pyplot as plt 
from tkinter import*
from tkinter import messagebox
from PIL import ImageTk,Image

root = Tk()
root.title('DATA ANALUSIS')
root.iconbitmap('combo-chart.png')
root.geometry("400x400")



#TWITTER KEYS
consumer_key = 'TieWMF0T7PRgeCRMK2wqpSGkc'
consumer_secret = '52cx1Gp4szYZ330HrBAod3mU32PpZdzSeGynBLaZJoxbCTFtdv'
access_token = '1015294450006757376-yPKrTjN1ay3Zlbb8fIvjoQnutYYQoy'
access_token_secret = 'TiVHn90MYwxhx8aHqHIOCUO9EbH5O0ygTvI1983vdM3Pg'




def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy API
    api = tweepy.API(auth)
    
    #get the name of the spreadsheet we will write to
    fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase.decode('utf-8')))

    #open the spreadsheet we will write to
    with open('%s.csv' % (fname), 'w', encoding="utf-8") as file:
        w = csv.writer(file)
        
        #write header row to spreadsheet
        w.writerow(['timestamp', 'tweet_text', 'username','sentiment', 'all_hashtags', 'followers_count'])
        pubic_tweets=tweepy.Cursor(api.search, q=hashtag_phrase.decode('utf-8') + ' -filter:retweets', lang="en", tweet_mode='extended').items(100)
        
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



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#engine.setProperty('voice',voices[2].id)


e=Entry(root,width=50,borderwidth=5,fg="grey")
e.grid(row=0,column=1,padx=5,pady=5)
a=e.get()


frame = LabelFrame(root)
frame.grid(row=5,column=1)





mylable=Label(root, text="ANALYSIS")
mylable.grid(row=0,column=0)







def open():
    top=Toplevel()
    top.geometry("400x400")
    btn=Button(top,text="close",padx=5,pady=5,command=top.destroy)
    btn.grid()

def speak(audio):
    engine.say(audio)
    engine.runAndWait() 

def myclick2():
    speak("hii beast")


def myclick3():
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
        return 'None'
    lable3=Label(text=query)
    lable3.grid(row=7,column=0)


def popup():
    response = messagebox.askyesno("hii","u sure")
    if response == 1:
        root.quit()

    





#THE ACTUAL QUERY
def click1():
    hashtag_phrase = '#'+a
    #DRIVER
    if __name__ == '__main__':
        search_for_hashtags(consumer_key.encode(encoding='utf-8'), consumer_secret.encode(encoding='utf-8'), access_token.encode(encoding='utf-8'), access_token_secret.encode(encoding='utf-8'), hashtag_phrase.encode(encoding='utf-8'))


        #Plotting piechart
        sample_data=pd.read_csv('C:\\Users\\BEAST\\Documents\\uhackathon\\'+hashtag_phrase.replace('#','')+".csv")
        #+hashtag_phrase.replace('#','')+".csv"
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
        n_perc=(pol1*100)/df.__len__()
        p_perc=(pol2*100)/df.__len__()
        negative_perc=(pol3*100)/df.__len__()
        values=[n_perc,p_perc,negative_perc]
        colors=['b','g','r']
        labels=['neutral percentage','positive percentage','negative percentsge']
        plt.pie(values, colors=colors, labels= values,counterclock=False, shadow=True)
        plt.title('Sentimental Analysis')
        plt.legend(labels,loc=3)
        plt.show()


    
    
    


myButton = Button(frame,text="click",padx=30,fg="red" ,command=click1)
myButton.grid(row=5,column=0)

myButton1 = Button(frame,text="voice",padx=30,fg="blue" ,command=myclick2)
myButton1.grid(row=5,column=1)

myButton1 = Button(frame,text="speak",padx=30,fg="blue" ,command=myclick3)
myButton1.grid(row=7,column=0)

buttonquit= Button(frame,text="quit",padx=30,command = popup)
buttonquit.grid(row=7,column=1)

button = Button(root,text="phone",padx=5,pady=5,command=open)
button.grid(row=6,column=1)

root.mainloop()

