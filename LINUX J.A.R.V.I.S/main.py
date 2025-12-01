import logging
from Jarvis import JarvisAssistant
import re
import os
os.environ['SDL_AUDIODRIVER'] = 'alsa'
import ollama
import random
import pprint
import datetime
import requests
import sys
import urllib.parse
import pyjokes
import time
import pyautogui
import pywhatkit
from PIL import Image
from Jarvis.config import config
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Jarvis.features.gui import Ui_MainWindow
#from Jarvis.config import config
from Jarvis.features.deepseek_integration import query_deepseek, clean_text
from Jarvis import JarvisAssistant
from Jarvis.database import create_table, save_conversation  # Import database functions

from Jarvis.database import create_table, save_conversation  # Import database functions
from Jarvis.chat_history_window import ChatHistoryWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread, pyqtSignal
import sqlite3

obj = JarvisAssistant()

# ================================ MEMORY ===========================================================================================================

GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey jarvis",
             "ok jarvis", "are you there"]
GREETINGS_RES = ["Hi Nigash, what can i do for you today", "Hey Nigash! Ready to assist you.",
                 "Greetings, Nigash. How may I assist you?", "how can i help you sir?"]

EMAIL_DIC = {
    'myself': 'atharvaaingle@gmail.com',
    'my official email': 'atharvaaingle@gmail.com',
    'my second email': 'atharvaaingle@gmail.com',
    'my official mail': 'atharvaaingle@gmail.com',
    'my second mail': 'atharvaaingle@gmail.com'
}

CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
# =======================================================================================================================================================

def speak(text):
    obj.tts(text)

    
def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    else:
        subprocess.run(['xdg-open', path])

class MainThread(QThread):
    openChatHistorySignal = pyqtSignal()
    closeChatHistorySignal = pyqtSignal()
    displaySignal = pyqtSignal(str, str, bool)
    exitSignal = pyqtSignal()
    showLoadingSignal = pyqtSignal()
    hideLoadingSignal = pyqtSignal()
    startupCompleteSignal = pyqtSignal()
    showLlmLoadingSignal = pyqtSignal()
    hideLlmLoadingSignal = pyqtSignal()

    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def handle_deepseek_stream(self, command, display_signal, api_key):
        buffer = ""
        full_response = ""
        sentence_starters = ["", " "]
        for chunk in query_deepseek(command, api_key):
            buffer += chunk
            full_response += chunk
            
            # Split the buffer into sentences
            sentences = re.split(r'(?<=[.!?])\s*', buffer)
            
            # Process all complete sentences
            for i in range(len(sentences) - 1):
                sentence = sentences[i]
                if sentence and (sentence[0] not in sentence_starters):
                    speak(sentence)
                    display_signal.emit(command, sentence, False)
            
            # The last part of the split is the new buffer
            buffer = sentences[-1]

        # Speak any remaining text in the buffer
        if buffer:
            speak(buffer)
            display_signal.emit(command, buffer, False)
        
        save_conversation(command, full_response)

    def startup(self):
        messages = [
            "Initializing Jarvis",
            "Starting all systems applications",
            "Installing and checking all drivers",
            "Caliberating and examining all the core processors",
            "Checking the internet connection",
            "Wait a moment sir",
            "All drivers are up and running",
            "All systems have been activated",
            "Now I am online"
             ]

        for message in messages:
            speak(message)
            self.displaySignal.emit("System", message, True)

        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour <= 12:
            speak("Good Morning")
        elif hour > 12 and hour < 18:
            speak("Good afternoon")
        else:
            speak("Good evening")

        c_time = obj.tell_time()
        speak(f"Currently it is {c_time}")
        self.displaySignal.emit("System", f"Currently it is {c_time}", True)
        speak("I am Jarvis. Online and ready sir. Please tell me how may I help you")
        self.displaySignal.emit("System", "I am Jarvis. Online and ready sir. Please tell me how may I help you", True)

    def TaskExecution(self):
        self.startup()
        
        while True:
            self.displaySignal.emit("System", "Started listening", True)
            command = obj.mic_input()
            if not command:
                continue
            command = command.lower()
            self.displaySignal.emit("System", f"Listening: {command}", True)
            print(f"🔹 You said: {command}")

            executed = False

            if re.search('today date', command):
                response = obj.tell_me_date()
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True
                
            elif "time" in command:
                response = f"Sir, the time is {obj.tell_time()}"
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            elif "open chat history" in command:
                speak("Let me fetch our past conversations for you sir!")
                self.openChatHistorySignal.emit()
                self.displaySignal.emit(command, "Opening chat history", False)
                executed = True
            
            elif "close chat history" in command:
                speak("Closing chat history as you requested, sir.")
                self.closeChatHistorySignal.emit()
                self.displaySignal.emit(command, "Closing chat history", False)
                executed = True

            elif "good bye jarvis" in command:
                speak("Goodbye, sir!")
                self.displaySignal.emit(command, "Goodbye, sir!", False)
                self.exitSignal.emit()
                break

            elif re.search('launch', command):
                if platform.system() == "Windows":
                    dict_app = {
                        'chrome': 'C:/Program Files/Google/Chrome/Application/chrome'
                    }
                else:
                    dict_app = {
                        'chrome': '/usr/bin/google-chrome'
                    }

                app = command.split(' ', 1)[1]
                path = dict_app.get(app)

                if path is None:
                    response = 'Application path not found'
                    speak(response)
                    self.displaySignal.emit(command, response, False)
                else:
                    response = f'Launching: {app} for you sir!'
                    speak(response)
                    obj.launch_any_app(path_of_app=path)
                    self.displaySignal.emit(command, response, False)
                executed = True

            elif command in GREETINGS:
                response = random.choice(GREETINGS_RES)
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            elif re.search('open', command):
                domain = command.split(' ')[-1]
                open_result = obj.website_opener(domain)
                response = f'Alright sir !! Opening {domain}'
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True
            
            elif re.search('search', command):
                domain = command.split(' ')[-1]
                open_result = obj.website_opener(domain)
                response = f'Alright sir !! Searching {domain}'
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            elif re.search('weather', command):
                city = command.split(' ')[-1]
                response = obj.weather(city=city, api_key=config.weather_api_key)
                if not response:
                    response = "Sorry, I couldn't get the weather for that city."
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            elif re.search('tell me about', command):
                topic = command.split(' ')[-1]
                if topic:
                    response = obj.tell_me(topic)
                    if not response:
                        response = f"Sorry, I couldn't find any information on {topic}."
                    speak(response)
                    self.displaySignal.emit(command, response, False)
                else:
                    response = "Sorry sir. I couldn't load your query from my database. Please try again"
                    speak(response)
                    self.displaySignal.emit(command, response, False)
                executed = True

            elif "buzzing" in command or "news" in command or "headlines" in command:
                news_res = obj.news(api_key=config.news_api_key)
                response = 'Source: The Times Of India. Todays Headlines are..'
                speak(response)
                for index, articles in enumerate(news_res):
                    pprint.pprint(articles['title'])
                    speak(articles['title'])
                    if index == len(news_res)-2:
                        break
                response = 'These were the top headlines, Have a nice day Sir!!..'
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            elif 'search google for' in command:
                obj.search_anything_google(command)
                self.displaySignal.emit(command, "Searching Google", False)
                executed = True
            
            elif "play some music" in command or "hit some music" in command:
                if platform.system() == "Windows":
                    music_dir = "D:\\Main Project\\3\\JARVIS-master\\Musics"
                else:
                    music_dir = os.path.join(os.path.expanduser('~'), 'Music')
                songs = os.listdir(music_dir)
                for song in songs:
                    open_file(os.path.join(music_dir, song))
                response = "Playing music"
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            elif 'youtube' in command:
                command_parts = command.split(' ')
                if len(command_parts) > 1:
                    video = ' '.join(command_parts[1:])
                    response = f"Okay sir, playing {video} on youtube"
                    speak(response)
                    pywhatkit.playonyt(video)
                    self.displaySignal.emit(command, response, False)
                else:
                    response = "Please specify what you want to play on YouTube."
                    speak(response)
                    self.displaySignal.emit(command, response, False)
                executed = True

            elif "email" in command or "send email" in command:
                sender_email = config.email
                sender_password = config.email_password
                
                try:
                    speak("Whom do you want to email sir ?")
                    recipient = obj.mic_input()
                    receiver_email = EMAIL_DIC.get(recipient)
                    if receiver_email:
                        speak("What is the subject sir ?")
                        subject = obj.mic_input()
                        speak("What should I say?")
                        message = obj.mic_input()
                        msg = 'Subject: {}\n\n{}'.format(subject, message)
                        obj.send_mail(sender_email, sender_password, receiver_email, msg)
                        response = "Email has been successfully sent"
                        speak(response)
                        self.displaySignal.emit(command, response, False)
                        time.sleep(2)
                    else:
                        response = "I couldn\'t find the requested person\'s email in my database. Please try again with a different name"
                        speak(response)
                        self.displaySignal.emit(command, response, False)
                except:
                    response = "Sorry sir. Couldn\'t send your mail. Please try again"
                    speak(response)
                    self.displaySignal.emit(command, response, False)
                executed = True

            elif "what is" in command or "who is" in command or "explain" in command or "can you say about" in command or "do you know about" in command or "do you know":
                answer = query_deepseek(command, config.gemini_api_key)
                response = answer
                cresponse=clean_text(response)
                speak(cresponse)
                jarvis.displayMessage(command, response)
                executed = True

            elif "what do i have" in command or "do i have plans" or "am i busy" in command:
                obj.google_calendar_events(command)
                response = "Fetching your calendar events"
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            elif "make a note" in command or "write this down" in command or "remember this" in command:
                speak("What would you like me to write down?")
                note_text = obj.mic_input()
                obj.take_note(note_text)
                response = "I\'ve made a note of that"
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            elif "close the note" in command or "close notepad" in command:
                response = "Okay sir, closing notepad"
                speak(response)
                if platform.system() == "Windows":
                    os.system("taskkill /f /im notepad++.exe")
                else:
                    # Assuming notepad++ is the process name on Linux as well
                    os.system("pkill notepad++")
                self.displaySignal.emit(command, response, False)
                executed = True

            elif "joke" in command:
                joke = pyjokes.get_joke()
                response = joke
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            elif "system usage" in command:
                sys_info = obj.system_info()
                response = sys_info
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            elif "where is" in command:
                place = command.split('where is ', 1)[1]
                current_loc, target_loc, distance = obj.location(place)
                city = target_loc.get('city', '')
                state = target_loc.get('state', '')
                country = target_loc.get('country', '')
                time.sleep(1)
                try:
                    if city:
                        response = f"{place} is in {state} state and country {country}. It is {distance} km away from your current location"
                    else:
                        response = f"{state} is a state in {country}. It is {distance} km away from your current location"
                    speak(response)
                    self.displaySignal.emit(command, response, False)
                except:
                    response = "Sorry sir, I couldn\'t get the coordinates of the location you requested. Please try again"
                    speak(response)
                    self.displaySignal.emit(command, response, False)
                executed = True

            elif "can you say my ip address" in command:
                ip = requests.get('https://api.ipify.org').text
                response = f"Your IP address is {ip}"
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            elif "switch the window" in command or "switch window" in command:
                response = "Okay sir, Switching the window"
                speak(response)
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")
                self.displaySignal.emit(command, response, False)
                executed = True

            elif "where i am" in command or "current location" in command:
                try:
                    city, state, country = obj.my_location()
                    response = f"You are in {city}, {state}, {country}"
                    self.displaySignal.emit(command, response, False)
                except:
                    response = "Sorry sir, I couldn\'t fetch your current location. Please try again"
                    self.displaySignal.emit(command, response, False)
                speak(response)
                executed = True

            elif "take screenshot" in command:
                speak("By what name do you want to save the screenshot?")
                name = obj.mic_input()
                screenshot_path = os.path.join(os.path.expanduser('~'), f"{name}.png")
                img = pyautogui.screenshot()
                img.save(screenshot_path)
                response = "Screenshot saved successfully"
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            elif "show me the screenshot" in command:
                try:
                    # This assumes the 'name' variable is still in memory from the last screenshot
                    screenshot_path = os.path.join(os.path.expanduser('~'), f"{name}.png")
                    img = Image.open(screenshot_path)
                    img.show()
                    response = "Here it is sir"
                    speak(response)
                    self.displaySignal.emit(command, response, False)
                    time.sleep(2)
                except (IOError, NameError):
                    response = "Sorry sir, I am unable to display the screenshot"
                    speak(response)
                    self.displaySignal.emit(command, response, False)
                executed = True

            elif "hide all files" in command or "hide this folder" in command:
                if platform.system() == "Windows":
                    os.system("attrib +h /s /d")
                    response = "Sir, all the files in this folder are now hidden"
                else:
                    response = "This feature is only supported on Windows."
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            elif "visible" in command or "make files visible" in command:
                if platform.system() == "Windows":
                    os.system("attrib -h /s /d")
                    response = "Sir, all the files in this folder are now visible to everyone. I hope you are taking this decision in your own peace"
                else:
                    response = "This feature is only supported on Windows."
                speak(response)
                self.displaySignal.emit(command, response, False)
                executed = True

            if not executed:
                self.handle_deepseek_stream(command, self.displaySignal, config.gemini_api_key)

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize history window
        self.history_window = None  
        # Connect the signal from `MainThread`
        startExecution.openChatHistorySignal.connect(self.openChatHistory)
        startExecution.closeChatHistorySignal.connect(self.closeChatHistory)
        startExecution.displaySignal.connect(self.displayMessage)
        startExecution.exitSignal.connect(self.close)
        startExecution.showLoadingSignal.connect(self.showLoading)
        startExecution.hideLoadingSignal.connect(self.hideLoading)


        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

        # Optional: Button to manually open chat history
        self.ui.chatHistoryButton = QPushButton("Chat History", self)
        self.ui.chatHistoryButton.setGeometry(50, 800, 150, 50)
        self.ui.chatHistoryButton.clicked.connect(self.openChatHistory)
        
        # --- Create loading GIF ---
        self.ui.loading_label = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.loading_label.setGeometry(QtCore.QRect(620, 350, 200, 200)) # Centered
        self.ui.loading_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.loading_movie = QtGui.QMovie("Jarvis/utils/images/loading.gif")
        self.ui.loading_label.setMovie(self.ui.loading_movie)
        self.ui.loading_label.hide()

        # --- Create program load GIF ---
        self.ui.program_load_label = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.program_load_label.setGeometry(QtCore.QRect(620, 350, 200, 200)) # Centered
        self.ui.program_load_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.program_load_movie = QtGui.QMovie("Jarvis/utils/images/program_load.gif")
        self.ui.program_load_label.setMovie(self.ui.program_load_movie)
        self.ui.program_load_label.hide()
        startExecution.startupCompleteSignal.connect(self.hideProgramLoad)
        
        # --- Create LLM loading GIF ---
        self.ui.llm_loading_label = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.llm_loading_label.setGeometry(QtCore.QRect(620, 350, 200, 200)) # Centered
        self.ui.llm_loading_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.llm_loading_movie = QtGui.QMovie("Jarvis/utils/images/loading_1.gif")
        self.ui.llm_loading_label.setMovie(self.ui.llm_loading_movie)
        self.ui.llm_loading_label.hide()
        startExecution.showLlmLoadingSignal.connect(self.showLlmLoading)
        startExecution.hideLlmLoadingSignal.connect(self.hideLlmLoading)

    def showLoading(self):
        """Shows the loading GIF and starts the animation."""
        self.ui.loading_label.show()
        self.ui.loading_movie.start()

    def hideLoading(self):
        """Hides the loading GIF and stops the animation."""
        self.ui.loading_label.hide()
        self.ui.loading_movie.stop()

    def showLlmLoading(self):
        """Shows the LLM loading GIF and starts the animation."""
        self.ui.llm_loading_label.show()
        self.ui.llm_loading_movie.start()

    def hideLlmLoading(self):
        """Hides the LLM loading GIF and stops the animation."""
        self.ui.llm_loading_label.hide()
        self.ui.llm_loading_movie.stop()

    def hideProgramLoad(self):
        """Hides the program load GIF and stops the animation."""
        self.ui.program_load_label.hide()
        self.ui.program_load_movie.stop()


    def openChatHistory(self):
        if self.history_window is None:
            self.history_window = ChatHistoryWindow()
        self.history_window.load_chat_history()
        self.history_window.show()

    def closeChatHistory(self):
        if self.history_window:
            self.history_window.close()
            self.history_window = None

    def startTask(self):
        # Movie for the first label
        self.ui.movie_1 = QtGui.QMovie("Jarvis/utils/images/live_wallpaper.gif")
        self.ui.label.setMovie(self.ui.movie_1)
        self.ui.movie_1.start()

        # Movie for the second label
        self.ui.movie_2 = QtGui.QMovie("Jarvis/utils/images/initiating.gif")
        self.ui.label_2.setMovie(self.ui.movie_2)
        self.ui.movie_2.start()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

    @pyqtSlot(str, str, bool)
    def displayMessage(self, user_input, jarvis_response, is_system_message=False):
        """Displays messages in the UI and saves them in the database."""
        if is_system_message:
            self.ui.textBrowser_3.setTextColor(QtGui.QColor("white"))
            self.ui.textBrowser_3.append(f"🤖 Jarvis: {jarvis_response}")
        else:
            self.ui.textBrowser_3.setTextColor(QtGui.QColor("white")),
            self.ui.textBrowser_3.append(f"🗣️ You: {user_input}")
            self.ui.textBrowser_3.append(f"🤖 Jarvis: {jarvis_response}")

            # Save to database
            save_conversation(user_input, jarvis_response)

if __name__ == '__main__':
    create_table()
    app = QApplication(sys.argv)
    jarvis = Main()
    jarvis.show()
    sys.exit(app.exec_())
