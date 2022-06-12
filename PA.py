#PA Program
#!/usr/bin/env python3

import speech_recognition as sr
from time import ctime
import os
import datetime
from gtts import gTTS
import webbrowser
from pyowm import OWM
import re
import sys
import os
import json
from playsound import playsound
import bs4
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen
#import googlemaps
import requests
#AIzaSyATAET-Zry2m0z88YCYFjL1DJ_Du7c5Ydg
re.compile('<title>(.*)</title>')
#Defining things
name="Jason"



def speak(audioString):
    print(audioString)
    tts=gTTS(text=audioString,lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")
def recordAudio():
    #Record Audio
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio=r.listen(source)

        #Speech recognition using gTTS
        data=" "
        try:
            data=r.recognize_google(audio)
            print("You said: "+data)
        except sr.UnknownValueError:
             print('Please restate')
        except sr.RequestError as e:
            playsound('318.wav')
        return data
def computer(data):
#Getting the weather
    if "weather" in data:
        reg_ex = re.search('current weather in (.*)', data)
        #city = reg_ex.group(1)
        city='Boston, US'
        owm=OWM(API_key='fdb056d4359e61625cad8f403a109c8a')
        obs=owm.weather_at_place(city)
        w=obs.get_weather()
        k=w.get_status()
        x=w.get_temperature(unit='celsius')
        speak('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree C'%(city,k,x['temp_max'],x['temp_min']))
#Getting Time
    if "time" in data:
       now=datetime.datetime.now()
       speak("Currently it is %d hundred hours and %d minutes"%(now.hour,now.minute))
    if "Hello computer" in data:
        now=datetime.datetime.now()
        playsound('Classic Intercom Whistle.mp3')
        if now.hour<12:
            speak("Good morning" + name)
        elif 12<=now.hour<18:
            speak("Good afternoon" +name)
        else:
            speak("Good evening" +name)
#Train and Communte Time
    if "commute" in data:
        endpoint='https://maps.googleapis.com/maps/api/directions/json?'
        destination="42.521496,-71.139404"
        origin="42.394973,-71.078548"
        API="AIzaSyATAET-Zry2m0z88YCYFjL1DJ_Du7c5Ydg"
        nav='origin=()&destination=()'.format(origin,destination)
        commute_url="https://maps.googleapis.com/maps/api/distancematrix/xml?origins=42.394973,-71.078548&destinations=42.521496,-71.139404+BC&mode=transit&language=fr-FR&key=AIzaSyATAET-Zry2m0z88YCYFjL1DJ_Du7c5Ydg"#"https://maps.googleapis.com/maps/api/distancematrix/xml?"+nav+"+BC&mode=transit&language=en-FR&key="+API
        commute_res=urllib.request.urlopen(commute_url).read()
        directions=json.loads(commute_res)
        speak(directions)
#Where is
    if "where is" in data:
        data=data.split(" ")
        location=data[2]
        speak("Hold on " + name + " I will show you where " + location + " is")
        url=("https://google.nl/maps/place/" + location + "/&amp;")
        webbrowser.open(url)
#Opening livestream (Beach)
    if "beach" in data:
        url=("https://www.youtube.com/watch?v=kbIATHfqP4g")
        webbrowser.open(url)
        playsound('032.wav')
#Close livestream (Beach)

#Top New from Google
    if 'news' in data:
        try:
            news_url="https://news.google.com/news/rss"
            URLObject = urllib.request.urlopen(news_url);
            xml_page = URLObject.read();
            URLObject.close();
            soup_page = BeautifulSoup(xml_page,"html.parser");
            news_list = soup_page.findAll("item");
            for news in news_list[:6]:
                #update=news.title.text.decode('utf-8')
                speak(news.title.text)
        except Exception as e:
                print(e)
#Launch applications
    if 'launch' in data:
        reg_ex = re.search('launch (.*)', data)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname+".app"
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
            speak('Application ready.')
# RED ALERT
    if "Red Alert" in data:
        playsound('redalert.mp3')
#Closing the Program
    if "shutdown" in data:
        playsound('Classic Intercom Whistle.mp3')
        sys.exit()
#initialization
playsound('Classic Intercom Whistle.mp3')
while 1:
    data=recordAudio()
    computer(data)

