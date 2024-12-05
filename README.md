# **Robo: Voice Assistant Mega Project**  
### 🌟 _"My First Mega Project, and I love it!"_ 🌟

---

## **Overview**  
Robo is a Python-based voice assistant that can:
- Recognize speech commands
- Open websites
- Play songs from a custom library
- Provide audio feedback using text-to-speech

This project demonstrates how Python can be used to build a simple yet powerful AI-powered assistant.

---

## **Features**  
- 🎙️ **Voice Commands**: Recognizes and executes spoken commands  
- 🗣️ **Text-to-Speech**: Responds with verbal feedback using `gTTS`  
- 🌐 **Website Automation**: Opens popular websites like Google, YouTube, Facebook  
- 🎵 **Music Playback**: Plays songs from a custom music library  
- ⚠️ **Error Handling**: Gracefully handles unknown commands and errors  

---

## **Installation**  

### 1. Clone the Repository  
```bash
git clone https://github.com/Mustafaadeel1/Maga_Project_ROBO-.git
cd Maga_Project_ROBO-
```
2. Install Dependencies
Install the required Python libraries:

* bash Copy code
```bash
pip install -r requirements.txt
```
* If the `requirements.txt` file doesn’t exist, install the libraries manually:


* bash
Copy code
```bash
pip install speechrecognition webbrowser pyttsx3 gtts pygame
```
3. Set Up the Music Library
Create a file named musicLibrary.py in the same folder as the project and add your favorite songs:

* python
Copy code 
# Example 
`musicLibrary.py`
```bash
music = {
    "shape of you": "https://example.com/shape_of_you",
    "perfect": "https://example.com/perfect",
}
```
# Usage
### Run the Program
```bash
python robo.py
```
### Commands
* Wake Word: `Say robo` to activate the assistant
* Open Websites: `Say open [website name] (e.g., open google)`
* Play Songs: `Say play [song name]` (e.g., play shape of you)
* Stop Songs: `Say stop the song or close the song`
* Shutdown Robo: `Say robo off`
# Project Structure
```

Maga_Project_ROBO-
│
├── robo.py               # Main program file
├── musicLibrary.py       # Custom music library (create this manually)
├── README.md             # Project documentation
├── requirements.txt      # List of dependencies
└── temp.mp3              # Temporary audio file (created during execution)
```
# Customization
### Add More Websites
__Edit the services dictionary in robo.py to include more websites:__

```python
Copy code
services = {
    "twitter": "https://twitter.com",
    "instagram": "https://instagram.com",
}
```
### Add More Songs
__Add more entries in musicLibrary.py with valid URLs:__

```python
Copy code
music = {
    "blinding lights": "https://example.com/blinding_lights",
    "levitating": "https://example.com/levitating",
}
```
# Future Improvements
* 🔧 Add functionality to directly manage browser tabs
* 🎤 Improve speech recognition with advanced models
* 🎶 Support local file music playback
