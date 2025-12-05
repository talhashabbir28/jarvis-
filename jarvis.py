import os
import webbrowser
import requests
import sounddevice as sd
import wavio
import speech_recognition as sr
from gtts import gTTS
from openai import OpenAI
import musicLibrary  


newsapi = "a96f89a71c84e259fbfee8f424225ad1"
openai_api_key = "your key"



def speak(text):
    """Convert text to speech and play it"""
    tts = gTTS(text)
    tts.save("temp.mp3")
    os.system("start temp.mp3" if os.name == "nt" else "afplay temp.mp3")  
    os.remove("temp.mp3")

def record_audio(duration=5, fs=44100):
    """Record audio using sounddevice and return recognized text"""
    print("Listening...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write("temp.wav", recording, fs, sampwidth=2)

    recognizer = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Google Speech Recognition error: {e}")
            return ""

def aiProcess(command):
    """Send command to OpenAI API and get response"""
    client = OpenAI(api_key=openai_api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

def processCommand(c):
    """Handle different types of commands"""
    c = c.lower()
    
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = " ".join(c.split(" ")[1:])
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in your library")
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])[:5]  # top 5 news
            for article in articles:
                speak(article["title"])
        else:
            speak("Sorry, I could not fetch the news")
    else:
        output = aiProcess



