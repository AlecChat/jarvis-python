import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import platform
import subprocess

# Optional: Your own song library
import musicLibrary 

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech(timeout=4):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=timeout)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Google speech service is down.")
        return ""

def open_app(app_name):
    system = platform.system()

    apps = {
        "notepad": "notepad",
        "calculator": "calc",
        "chrome": "chrome",
        "firefox": "firefox",
        "vs code": "code"
    }

    matched_app = apps.get(app_name)
    if not matched_app:
        speak(f"I don't know how to open {app_name}")
        return

    speak(f"Opening {app_name}")
    if system == "Windows":
        os.system(f"start {matched_app}")
    elif system == "Darwin":
        subprocess.Popen(["open", "-a", matched_app])
    elif system == "Linux":
        subprocess.Popen([matched_app])
    else:
        speak("Unsupported OS")

def processCommand(command):
    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open spotify" in command:
        webbrowser.open("https://open.spotify.com/")
    elif command.startswith("play"):
        song = command.split(" ", 1)[1]
        link = musicLibrary.library.get(song)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song}")
    elif command.startswith("open"):
        app_name = command.replace("open", "").strip()
        open_app(app_name)
    else:
        speak("Sorry, I don't understand that command.")


if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        print("Listening for wake word...")
        wake_word = recognize_speech(timeout=3)
        if wake_word == "jarvis":
            speak("Say what to do, sir.")
            command = recognize_speech(timeout=5)
            if command:
                processCommand(command)
