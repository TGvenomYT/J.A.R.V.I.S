import speech_recognition as sr
import threading
from gtts import gTTS
import pygame
from pynput import keyboard
import os
import sys

from Jarvis.features import date_time
from Jarvis.features import launch_app
from Jarvis.features import website_open
from Jarvis.features import weather
from Jarvis.features import wikipedia
from Jarvis.features import news
from Jarvis.features import send_email
from Jarvis.features import google_search
from Jarvis.features import google_calendar
from Jarvis.features import note
from Jarvis.features import system_stats
from Jarvis.features import loc
from Jarvis.features.deepseek_integration import query_deepseek

# Context manager to suppress stderr for noisy C libraries
class SuppressStderr:
    def __enter__(self):
        self.devnull = open(os.devnull, 'w')
        self.old_stderr = sys.stderr
        sys.stderr = self.devnull

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stderr = self.old_stderr
        self.devnull.close()


class JarvisAssistant:
    def __init__(self):
        """Initialize the assistant."""
        with SuppressStderr():
            pygame.init()
            pygame.mixer.init()
        self.speech_lock = threading.Lock()
        self.stop_speaking = False
        self.listener = None

    def mic_input(self):
        """
        Fetch input from mic.
        Returns: user's voice input as text if recognized, False if failed.
        """
        try:
            r = sr.Recognizer()
            with SuppressStderr():
                with sr.Microphone() as source:
                    print("🎙️ Listening....")
                    #r.pause_threshold = 1
                    r.energy_threshold = 4000
                    audio = r.listen(source, phrase_time_limit=10)
            try:
                print("🔎 Recognizing...")
                command = r.recognize_google(audio, language='en-in').lower()
                print(f'You said: {command}')
            except Exception:
                print('⚠️ Please try again')
                command = self.mic_input()
            return command
        except Exception as e:
            print(e)
            return False

    def tts(self, text):
        """
        Speak text fluently and stop when Ctrl is pressed.
        """
        if not text:
            print("Error in tts: No text to speak")
            return
            
        self.stop_speaking = False

        def on_press(key):
            if key == keyboard.Key.ctrl:
                print("Ctrl key pressed! Stopping speech...")
                self.stop_speaking = True
                pygame.mixer.music.stop()
                if self.listener:
                    self.listener.stop()
                return False

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

        with self.speech_lock:
            try:
                tts = gTTS(text=text, lang='en')
                tts.save("speech.mp3")
                with SuppressStderr():
                    pygame.mixer.music.load("speech.mp3")
                    pygame.mixer.music.play()

                while pygame.mixer.music.get_busy() and not self.stop_speaking:
                    pygame.time.Clock().tick(10)

            except Exception as e:
                print(f"Error in tts: {e}")
            finally:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                if os.path.exists("speech.mp3"):
                    try:
                        os.remove("speech.mp3")
                    except PermissionError:
                        print("Could not remove speech.mp3, file in use.")
                if self.listener:
                    self.listener.stop()


    def tell_me_date(self):
        return date_time.date()

    def tell_time(self):
        return date_time.time()

    def launch_any_app(self, app_name):
        """Launch any application by name."""
        return launch_app.launch_app(app_name)

    def website_opener(self, domain):
        """Open a website based on the domain."""
        return website_open.website_opener(domain)

    def weather(self, city, api_key):
        """Fetch weather for a given city."""
        try:
            return weather.fetch_weather(city, api_key)
        except Exception as e:
            print(e)
            return False

    def tell_me(self, topic):
        """Fetch Wikipedia information."""
        return wikipedia.tell_me_about(topic)

    def news(self, api_key):
        """Fetch top news of the day."""
        return news.get_news(api_key)

    def send_mail(self, sender_email, sender_password, receiver_email, msg):
        """Send an email."""
        return send_email.mail(sender_email, sender_password, receiver_email, msg)

    def google_calendar_events(self, text):
        """Fetch Google Calendar events."""
        service = google_calendar.authenticate_google()
        date = google_calendar.get_date(text)
        return google_calendar.get_events(date, service) if date else None

    def search_anything_google(self, command):
        google_search.google_search(command)

    def take_note(self, text):
        note.note(text)

    def system_info(self):
        return system_stats.system_stats()

    def location(self, location):
        current_loc, target_loc, distance = loc.loc(location)
        return current_loc, target_loc, distance

    def my_location(self):
        city, state, country = loc.my_location()
        return city, state, country