# My First maga project i love it :)
import speech_recognition as sr
import webbrowser
import pyttsx3
from gtts import gTTS
import pygame
import os
import musicLibrary  # Import the custom music library
import sys

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Store active browser windows for later closing (Note: Only track URLs in the current session)
open_tabs = {}

# Define the available services and their URLs
services = {
    "google": "https://google.com",
    "facebook": "https://facebook.com",
    "youtube": "https://youtube.com",
    "linkedin": "https://linkedin.com",
    "github": "https://github.com",
}

# Initialize pygame mixer for playing music
pygame.mixer.init()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def close_song(song_name=None):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()  # Stop the song
        speak(f"Song {song_name} is stopped." if song_name else "Song is stopped.")
    else:
        speak("No song is currently playing.")

def open_service(service_name):
    if service_name in services:
        url = services[service_name]
        webbrowser.open(url)
        open_tabs[service_name] = url  # Add the service to open tabs
        speak(f"Opening {service_name}.")
    else:
        speak(f"Sorry, I don't know how to open {service_name}.")

def processCommand(c):
    c = c.lower()

    if "robo off" in c:
        speak("Shutting down Robo.")
        sys.exit(0)  # Exit the program with a success status code

    # Check for open commands for services
    for service in services.keys():
        if f"open {service}" in c:
            open_service(service)
            return

    # Handle music play command
    if c.startswith("play"):
        try:
            song = " ".join(c.split(" ")[1:])  # Extract song name from user command
            music_lower = {key.lower(): value for key, value in musicLibrary.music.items()}

            if song in music_lower:
                link = music_lower[song]
                webbrowser.open(link)
                open_tabs[song] = link  # Add the song to open tabs list
                speak(f"Playing {song}.")
            else:
                speak(f"Sorry, I couldn't find the song '{song}' in your library.")
        except Exception as e:
            speak(f"An error occurred while playing music: {e}")
    
    # Handle stop song
    elif "close the song" in c or "stop the song" in c:
        close_song()

    # Handle close specific browser tabs (Note: This will just provide feedback)
    for service in services.keys():
        if f"close {service}" in c:
            speak(f"Please manually close {service}.")
            return

    # Handle close all browser tabs command (Note: This will just provide feedback)
    if "close all browser tabs" in c:
        speak("Please manually close all browser tabs.")
        open_tabs.clear()  # Clear the open_tabs dictionary

    else:
        speak("I don't understand that command.")

if __name__ == "__main__":
    speak("Initializing Robo....")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            word = recognizer.recognize_google(audio)
            if word.lower() == "robo":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except SystemExit:
            print("Exiting...")
            break  # Break the loop and exit the program
        except Exception as e:
            print(f"Error: {e}")
