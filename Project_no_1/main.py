import streamlit as st
import speech_recognition as sr
import webbrowser
import pygame
import os
import threading
import time
import queue
from gtts import gTTS

# Initialize components
recognizer = sr.Recognizer()
pygame.mixer.init()

services = {
    "google": "https://google.com",
    "facebook": "https://facebook.com",
    "youtube": "https://youtube.com",
    "linkedin": "https://linkedin.com",
    "github": "https://github.com",
}

# Session state setup
if "history" not in st.session_state:
    st.session_state.history = []
if "running" not in st.session_state:
    st.session_state.running = False
if "status" not in st.session_state:
    st.session_state.status = "🔴 Inactive"

command_queue = queue.Queue()

def speak(text):
    try:
        tts = gTTS(text)
        tts.save('temp.mp3')
        pygame.mixer.music.load('temp.mp3')
        pygame.mixer.music.play()
        command_queue.put(("ROBO", text))
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
        os.remove("temp.mp3")
    except Exception as e:
        command_queue.put(("Error", f"Text-to-speech error: {str(e)}"))

def process_command(command):
    try:
        if "open" in command:
            for service_name in services:
                if service_name.lower() in command.lower():
                    webbrowser.open(services[service_name])
                    speak(f"Opening <span class='service-name'>{service_name}</span> for you.")
                    return
            speak("Service not found in database.")
        else:
            speak("Command not recognized.")
    except Exception as e:
        command_queue.put(("Error", f"Processing error: {str(e)}"))

def start_robo():
    try:
        speak("Initializing Robo....")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            while st.session_state.running:
                try:
                    command_queue.put(("STATUS", "🎤 Listening..."))
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio)
                    command_queue.put(("USER", command))
                    process_command(command)
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    command_queue.put(("Error", str(e)))
    except Exception as e:
        command_queue.put(("Error", f"Initialization error: {str(e)}"))

# Enhanced UI with animated elements
st.set_page_config(page_title="ROBO Assistant", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
:root {
    --primary: #FF6B6B;
    --secondary: #4ECDC4;
    --background: #1a1a1a;
}

body {
    background-color: var(--background);
    color: white;
}

.title-container {
    text-align: center;
    padding: 2rem;
    background: rgba(0, 0, 0, 0.9);
    border-radius: 20px;
    margin: 2rem auto;
    box-shadow: 0 8px 30px rgba(255,107,107,0.3);
    border: 2px solid var(--primary);
}

.title-text {
    font-size: 3.5em;
    font-weight: 800;
    background: linear-gradient(45deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient 3s ease infinite;
    position: relative;
    margin: 0;
    padding: 1rem;
}

@keyframes gradient {
    0% {background-position: 0% 50%}
    50% {background-position: 100% 50%}
    100% {background-position: 0% 50%}
}

/* Modified command boxes */
.command-box {
    padding: 1.5rem;
    margin: 1rem 0;
    background: #000000 !important;
    border-radius: 15px;
    border-left: 5px solid var(--primary);
    border: 1px solid white !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}

.command-box:hover {
    transform: translateX(10px);
    box-shadow: 0 6px 20px rgba(255,107,107,0.4);
}

/* Modified response boxes */
.response-box {
    padding: 1.5rem;
    margin: 1rem 0;
    background: #000000 !important;
    border-radius: 15px;
    border-left: 5px solid var(--secondary);
    border: 1px solid white !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}

.status-indicator {
    padding: 1rem;
    border-radius: 10px;
    background: #333;
    text-align: center;
    margin: 1rem 0;
    border: 2px solid var(--primary);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% {box-shadow: 0 0 0 0 rgba(78,205,196,0.4)}
    70% {box-shadow: 0 0 0 15px rgba(78,205,196,0)}
    100% {box-shadow: 0 0 0 0 rgba(78,205,196,0)}
}

/* Modified service cards */
.service-card {
    padding: 1.5rem;
    background: #000000;
    border-radius: 15px;
    text-align: center;
    transition: all 0.3s ease;
    border: 2px solid #ffffff;
    color: white !important;
    margin: 0.5rem;
}

.service-card h4 {
    color: white !important;
    border-bottom: 1px solid white;
    padding-bottom: 0.5rem;
    margin-bottom: 0.5rem;
}

.service-card small {
    color: #cccccc !important;
    font-size: 0.8em;
}

.service-name {
    background: #000000;
    color: white !important;
    padding: 0.2rem 0.5rem;
    border-radius: 5px;
    display: inline-block;
    margin: 0.2rem 0;
    border: 1px solid white;
}
</style>
""", unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.markdown("## 🤖 ROBO Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Start", key="start", use_container_width=True):
            if not st.session_state.running:
                st.session_state.running = True
                st.session_state.status = "🟢 Active"
                threading.Thread(target=start_robo).start()
    
    with col2:
        if st.button("🛑 Stop", key="stop", use_container_width=True):
            st.session_state.running = False
            st.session_state.status = "🔴 Inactive"
    
    st.markdown("### 📊 Live Status")
    st.markdown(f"""
    <div class="status-indicator">
        <h3>{st.session_state.status}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🌐 Services Database")
    for service, url in services.items():
        st.markdown(f"""
        <div class="service-card">
            <h4>{service.capitalize()}</h4>
            <small>{url}</small>
        </div>
        """, unsafe_allow_html=True)

# Main interface
st.markdown("""
<div class="title-container">
    <h1 class="title-text">🤖 ULTIMATE ROBO ASSISTANT ⚡</h1>
</div>
""", unsafe_allow_html=True)

# Real-time updates
while not command_queue.empty():
    entry = command_queue.get()
    if entry[0] == "STATUS":
        st.session_state.status = entry[1]
    else:
        st.session_state.history.append(entry)

# Interaction history
st.markdown("## 📜 Command History")
for entry in reversed(st.session_state.history):
    if entry[0] == "USER":
        st.markdown(f'<div class="command-box">👤 User: {entry[1]}</div>', unsafe_allow_html=True)
    elif entry[0] == "ROBO":
        st.markdown(f'<div class="response-box">🤖 ROBO: {entry[1]}</div>', unsafe_allow_html=True)
    elif entry[0] == "Error":
        st.markdown(f'<div class="command-box" style="border-color: #ff0000;">🚨 Error: {entry[1]}</div>', unsafe_allow_html=True)

# Service visualization
st.markdown("## 🌟 Featured Services")
cols = st.columns(len(services))
for i, (service, url) in enumerate(services.items()):
    with cols[i]:
        st.markdown(f"""
        <div class="service-card">
            <h3>{service.capitalize()}</h3>
            <p><small>{url}</small></p>
        </div>
        """, unsafe_allow_html=True)