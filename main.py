import pyttsx3
import speech_recognition as sr
import datetime
import os
import random
from random import randint
import wikipedia
import webbrowser
import pyjokes
import subprocess
import time
import pyautogui
import psutil
import winshell
import socket
from googleapiclient.discovery import build
import urllib.parse  
import requests






engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing....")
            query = r.recognize_google(audio, language="en-ur")
            print(f"User Said: {query}\n")
        except Exception as e:
            speak("Unable to recognize your voice...")
            return None
        return query


def get_username():
        pass
        
        # uname = takeCommand()
        # if uname:
        #     speak("Welcome Mister " + uname)
        # else:
        #     speak("I couldn't hear your response. Please tell me your name, Sir.")
        # speak("How can I help you, Sir?")       

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")
    speak("I am your Personal Assistant Japan.")

def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU is at " + usage)
    battery = str(psutil.sensors_battery())
    speak("Battery is at " + battery)
    
def shutdown_security():
    
    speak("Are you sure you want to shut down the system? Please say yes to confirm or no to cancel.")
    confirmation = takeCommand().lower()

    if confirmation:
        if "yes" in confirmation:
            speak("Shutting down the system. Please make sure all your applications are closed.")
            time.sleep(5)
            subprocess.call(["shutdown", "/s"])
        elif "no" in confirmation:
            speak("Shutdown cancelled.")
        else:
            speak("Sorry, I didn't understand. Shutdown cancelled.")
    else:
        speak("I couldn't hear your response. Shutdown cancelled.")

def rock():
    you = int(input("Please enter you choice /n 1: Rock /n 2: Paper /n 3: Scissor"))
    shapes = ["1: Rock, 2: Paper, 3: Scissor"]
    if you not in shapes:
        print("Please enter a valid Input")
        exit
    comp = random.randint(1,3)
    print("You choose ",you)
    print("Computer choose",comp)
    if (you==1) and (comp==3) or (you==2) and (comp==1) or (you==3) or (comp ==2):
        speak("Congratulations You Won!")
    elif (you==comp):
        speak("Match Tied")
    else:
        speak("You lose")

def count_timer():
    user = int(input("Enter time in Seconds"))
    while user:
        min,secs = divmod(user,60)
        timer = '{:02d}:{:02d}'.format(min,secs)
        print(timer,end = "\r")
        time.sleep(1)
        user -= 1
        print("\n")
    
def guess():
    start = 1
    end = 1000
    value = randint(start,end)
    print("The computer choose the number b/w the ",start, "and", end)
    guess = None
    while guess != value:
        text = input("Enter Your Value")
        guess = int(text)
        if guess < value:
            speak('The value is Higher')
        elif guess > value:
            speak("The value is lower")
        else:
            speak("Congratulations You Won")

def youtube_search(query):
    try:
        youtube = build('youtube', 'v3', developerKey='AIzaSyCOEuhuJZwFmTrBGgTCso-eqsg197OvC6k')  
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=1
        )
        response = request.execute()
        
        if 'items' not in response or len(response['items']) == 0:
            speak("Sorry, I couldn't find any videos for your search.")           
            return None
        item = response['items'][0]
        title = item['snippet']['title']
        video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        speak(f"Found a video: {title}. Now opening it.")
        webbrowser.open(video_url) 
        time.sleep(3) 
        speak(f"Your video is now playing. Cheers!")
        return title, video_url
        
    except Exception as e:
        speak("Sorry, there was an error while searching for the video.")
        print(f"Error: {e}")
        return None
        

    
def play_game():
    speak("Which game would you like to play, Sir? We have three options: Rock Paper Scissors, Guess the Number, and Countdown Timer.")
    game_choice = takeCommand()  
    
    if game_choice:
        game_choice = game_choice.lower()  
        
        
        if "rock paper scissors" in game_choice or "rock" in game_choice:
            speak("Okay, let's play Rock, Paper, Scissors.")
            rock()  
        elif "guess the number" in game_choice or "guess" in game_choice:
            speak("Let's play Guess the Number!")
            guess()  
        elif "countdown" in game_choice or "timer" in game_choice:
            speak("Starting Countdown Timer.")
            count_timer()  
        else:
            speak("Sorry, I didn't understand that. Please choose a valid game.")
            play_game()  
    else:
        speak("I couldn't hear your response. Please try again.")
        play_game() 

def get_news():
    api_key = "ccec2ae3ced143f19cfe47f03cc8645c"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    news_data = response.json()

    if news_data['status'] == 'ok':
        articles = news_data['articles']
        speak("Here are the top news stories.")
        for article in articles[:5]:  # Get top 5 news stories
            title = article['title']
            description = article['description']
            speak(f"Title: {title}")
            speak(f"Description: {description}")
            print(f"Title: {title}\nDescription: {description}\n")
    else:
        speak("Sorry, I couldn't fetch the news.") 

def get_weather():
    speak("Please tell me the city you want to know about weather sir.")
    city = takeCommand()
    if city:
        api_key = "26889781b480fa3b4e426ba68c0a6a7f"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data['cod'] == 200:
            temp = data['main']['temp']
            weather_description = data['weather'][0]['description']
            speak(f"The current temperature in {city} is {temp} degrees Celsius with {weather_description}.")
        else:
            speak(f"Sorry, I couldn't fetch the weather for {city}.")
    else:
        speak("I didn't catch the city name. Please try again.")

wishme()
get_username()

while True:
    order = takeCommand()
    if order:
        order = order.lower()  

        if "how are you" in order or"how r u" in order:
            speak("I am fine. Thank you!")
            speak("How are you, Sir?")
        elif 'fine' in order or "good" in order or "i am fine" in order:
            speak("It's good to know that you are fine.")
        elif "who am i" in order.lower() or "who i am " in order.lower():
            speak("If you can talk, then surely you are human.")
        elif "who are you" in order.lower() or "who r u" in order.lower():
            speak("I am your Personal Assistant. You can called me  Japan.")
        elif "I love you" in order or "I like you" in order:
            speak("Oh, that's amazing. But I am only your Personal Assistant . Sorry.")
        elif "will you be my girlfriend" in order or "become my girlfriend" in order:
            speak("I'm not sure about that. Please give me some more time.")
        elif "what is your name" in order:
            speak("My friends call me Japan.")
        elif "will you marry me" in order or "marry me " in order:
            speak("I would, but I think my Wi-Fi connection would get jealous.")
        elif "open notepad" in order:
            npath = "C:\\Windows\\System32\\notepad.exe"
            os.startfile(npath)
        
        elif "wikipedia" in order:
            speak("Searching...")
            order = order.replace('wikipedia'," ")
            results = wikipedia.summary(order,sentences = 2)
            speak("According to wikipedia")
            speak(results)
        elif 'open google' in order:
            speak("Here you go to Google, Sir.")
            webbrowser.open("https://www.google.com")
        elif 'open youtube' in order:
            speak("Here you go to YouTube, Sir.")
            webbrowser.open("https://www.youtube.com")
        elif 'open github' in order:
            speak("Here you go to GitHub, Sir.")
            webbrowser.open("https://github.com")
        elif 'open w3school' in order:
            speak("Here you go to W3Schools, Sir.")
            webbrowser.open("https://www.w3schools.com")
        elif 'open chatgpt' in order:
            speak("Here you go to ChatGPT, Sir.")
            webbrowser.open("https://chat.openai.com")  
        elif 'open amazon' in order:
            speak("Here you go to Amazon, Sir.")
            webbrowser.open("https://www.amazon.com")
        elif 'open daraz' in order:
            speak("Here you go to Daraz, Sir.")
            webbrowser.open("https://www.daraz.com")
        elif 'open ebay' in order:
            speak("Here you go to eBay, Sir.")
            webbrowser.open(f"https://www.ebay.com+{order}")
        elif "open camera" in order:
            speak("Opening the camera, Sir.")
            os.system("start microsoft.windows.camera:")
        elif 'open ms word' in order:
            speak("Opening Ms Word, Sir,")
            subprocess.Popen([r"C:\\Program Files (x86)\\Microsoft Office\\Office12\WINWORD.EXE"])
        elif 'open ms excel' in order:
            speak("Opening Ms Excel, Sir,")
            subprocess.Popen([r"C:\\Program Files (x86)\\Microsoft Office\\Office12\\EXCEL.EXE"])
        elif 'open ms powerpoint' in order:
            speak("Opening Ms Powerpoint, Sir,")
            subprocess.Popen([r"C:\\Program Files (x86)\\Microsoft Office\\Office12\\POWERPNT.EXE"])

        elif 'where is' in order:
            order = order.replace("where is", "").strip()  
            if order: 
                speak(f"Here is the location for {order}.")
                encoded_order = urllib.parse.quote(order)
                webbrowser.open(f"https://www.google.com/maps/search/?api=1&query={encoded_order}+Pakistan")
            else:
                speak("Please specify a location.")
        elif 'write a note' in order:
            speak("What should I write, Sir?")
            note = takeCommand()

    
            if note:
                with open("A.I.txt", 'w') as file:
                    speak("Sir, should I write the date and time as well?")
                    sn = takeCommand()

            
                  
                    if sn and ('yes' in sn.lower() or 'sure' in sn.lower() or 'yeah' in sn.lower()): 
                        strTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        file.write(f"{strTime}\n") 
                    file.write(note + "\n")  
                    speak("Done, Sir.") 
            else:
                speak("I didn't catch that, Sir. Please tell me what to write.")

        elif 'show note' in order:
            speak("Showing note, Sir...")
            with open("A.I.txt", 'r') as file:  
              
                speak(note)  
                speak("Done, Sir.")

        elif 'joke' in order:
            speak((pyjokes.get_joke(language="en",category="neutral")))
        elif 'the time' in order or 'current time' in order:
            strTime = datetime.datetime.now().strftime("%H:%M") 
            speak(f"Well, the time is {strTime}")  
        elif 'shutdown' in order or 'trun off' in order:
            speak("Hold on sir. Your System going to shutdown")
            speak("Make Sure all your application are closed")
            time.sleep(5)
            subprocess.call(["shutdown",'/s'])
        elif 'restart ' in order:
            speak("Your System going to restarted sir")
            subprocess.call(["shutdown",'/r'])
        elif 'hibernate' in order:
            speak("Hybernating....")
            subprocess.call(["shutdown","/h"])
        elif 'sign out' in order or 'log off' in order:
            speak("Make sure you all applications are closed before sign you out!")
            subprocess.call(["shutdown","/i"])
        elif 'switch window' in order:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")
        elif 'take a screenshot' in order or 'take screenshot' in order:
            speak("sir,Please tell me the name to save a Screenshot")
            file_name = takeCommand()
            speak("Sir,Please  Hold a scrren ")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{file_name}.png")
            speak("Screenshot Captured Sir!")
        elif 'cpu status' in order or 'tell my device status' in order:
            cpu()
        elif 'thanks' in order or 'thank you ' in order:
            speak("You're Welcome Sir! HAve a nice Day Sir!") 
        elif 'empty recycle bin' in order:
            winshell.recycle_bin().empty(confirm=True,show_progress=True,sound=True)
            speak("Recycle Bin is recycled ")  
        elif 'ip' in order or 'my ip' in order:
            host = socket.gethostname()
            ip = socket.gethostbyname(host)
            speak("Your ip address is "+ ip)
        elif 'bmi' in order or 'calculate my bmi ' in order:
            speak("Pleae tell me your height in centimeters")
            height = takeCommand()
            speak("Please tell me your weight in kilograms")
            weight = takeCommand()
            height = float(height)/100
            BMI = float(weight)/(height*height)
            speak("Your Body Mass Index is " + str(BMI))
            if BMI > 0:
                if BMI <=16:
                    speak("You're severally under weight")
                elif  BMI <=18.5:
                    speak("You're underweight")
                elif BMI <=25:
                    speak("You are Healthy")
                elif BMI <=30:
                    speak("You are over weight")
                else:
                    speak("You're severally over weight")
            else:
                speak("Enter Valid Details Sir")

        elif 'play game' in order or 'games' in order or 'play games' in order:
            play_game()

        elif "search for" in order:
            search_query = order.replace("search for", "").strip()  
            if search_query:
                speak(f"Searching for {search_query} on YouTube.")
                results = youtube_search(search_query)  
                if results:
                    for idx, result in enumerate(results):
                        print(f"Result {idx + 1}: {result['title']}-{result['url']}")
                        speak(f"{idx + 1}. {result['title']}")  
                    speak("Opening the first video now.")
                    webbrowser.open(results[0]['url']) 
                else:
                    speak("Sorry, I couldn't find any results.")
            else:
                speak("Sorry, I didn't catch the search term.")
        elif "latest news" in order or "tell me news" in order:
            get_news()
        elif "tell weather" in order or "weather update" in order:
            get_weather()
        elif "okay bye" in order or "close" in order:
            break
       
      
        
             
   







        
        



 
