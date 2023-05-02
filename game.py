import pyaudio
import wave
from threading import Thread


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import random
import time


import speech_recognition as sr


with open(Words.txt', 'r') as file:
    text = file.read()


# Split the text into a list of words
words = text.split()
word = None


def get_rando_word():
    return random.choice(words)






PATH = "output3.wav"


class IntroApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.word = worder




    def getout(self, instance):
        self.stop()




    def build(self):
        # Create a vertical box layout to hold the label and button
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)


        # Create a label widget with the word to be displayed
        self.label = Label(text=f'Your word is {self.word}', font_size=24, halign='center')


        # Create a button widget with the message to be displayed
        button = Button(text='Click this button to continue', font_size=20, size_hint=(None, None), size=(200, 50), background_color=(0, 0.7, 0.5, 1))
        button.bind(on_press=self.getout)
       


        # Add the label and button widgets to the layout
        layout.add_widget(self.label)
        layout.add_widget(button)


        # Return the layout as the root widget
        return layout




class CountdownApp(App):
   
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seconds = 0
        self.timer_event = None
        self.recording_thread = None
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False
       
    def start_countdown(self, seconds):
        self.seconds = seconds
        self.root_label.text = str(self.seconds)
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update, 1)
       
    def update(self, dt):
        self.seconds -= 1
        self.root_label.text = str(self.seconds)
        if self.seconds == 0:
            self.stop_recording()
            self.timer_event.cancel()
            self.root_label.text = 'Countdown finished!'
       
    def start_recording(self):
        self.is_recording = True
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.frames = []
        print("Recording started...")
       
    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            print("Recording stopped...")
            wf = wave.open(PATH, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            print("Recording saved as output3.wav")
            self.stop()
       
    def record_audio(self):
        self.start_recording()
        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)
           
    def start_recording_thread(self):
        self.recording_thread = Thread(target=self.record_audio)
        self.recording_thread.start()


    def build(self):
        layout = BoxLayout(orientation='vertical')
       
        self.root_label = Label(text='Select countdown time:')
        layout.add_widget(self.root_label)
       
        buttons_layout = BoxLayout(orientation='horizontal')
        button_30 = Button(text='10 seconds', on_press=lambda _: self.start_countdown(10))
        button_60 = Button(text='30 seconds', on_press=lambda _: self.start_countdown(30))
        button_120 = Button(text='1 minute', on_press=lambda _: self.start_countdown(60))
       
        buttons_layout.add_widget(button_30)
        buttons_layout.add_widget(button_60)
        buttons_layout.add_widget(button_120)
       
        layout.add_widget(buttons_layout)
       
        return layout




class FinalizerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        audio = None
        r = sr.Recognizer()
        PATH = "output3.wav"


        harvard = sr.AudioFile(PATH)


        with harvard as source:
            audio = r.record(source)
       
        self.spoken = r.recognize_google(audio)
        print(self.spoken)
        self.count1 = False
        self.count2 = False

    def yes_1(self, instance):
        self.count1 = True
       
    def yes_2(self, instance):
        self.count2 = True
           


    def confirm(self, instance):
        if (self.count1 == True or self.count2 == True) and worder in self.spoken.split(): #changed and to or
            self.scorer = True
        else:
            self.scorer = False
        print(self.count1, self.count2, worder in list(self.spoken))
        print(self.spoken.split())
        self.stop()


   


    def build(self):
        # Create a vertical box layout to hold the label and buttons
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)


        # Create a label widget with the message to be displayed
        label = Label(text='Did you finish the task and say the word?')


        # Create two button widgets to confirm the completion of the task
        button1 = Button(text='Yes, I finished the task', font_size=16, size_hint=(None, None), size=(250, 50), background_color=(0, 0.7, 0.5, 1))
        button1.bind(on_press=self.yes_1)


        button2 = Button(text='Yes, I said the word', font_size=16, size_hint=(None, None), size=(250, 50), background_color=(0, 0.7, 0.5, 1))
        button2.bind(on_press=self.yes_2)


        # Add the label and button widgets to the layout
        layout.add_widget(label)
        layout.add_widget(button1)
        layout.add_widget(button2)


        # Add a confirm button widget to the layout
        confirm_button = Button(text='Confirm', font_size=16, size_hint=(None, None), size=(250, 50), background_color=(0.5, 0.5, 0.5, 1))
        confirm_button.bind(on_press=self.confirm)
        layout.add_widget(confirm_button)
        # Return the layout as the root widget
        return layout


class ScoreDisplay(App):
    def __init__(self, scorer, score, **kwargs):
        super().__init__(**kwargs)
        self.scorer = scorer
        self.score = score
        if self.scorer:
            self.score  += 1
            print(self.score)
    def build(self):
        your_score = self.score
        label = Label(text=f"The score for you is {your_score}")
        return label


if __name__ == '__main__':
    score = 0
    scorer = False
    worder = get_rando_word().lower()
    app_1 = IntroApp()
    #app = CountdownApp()
    #app2 = FinalizerApp()
    #app3 = ScoreDisplay()
    app_1.run()
    app = CountdownApp()
    app.start_recording_thread()
    app.run()
    time.sleep(1)
    app2 = FinalizerApp()
    app2.run()
    app3 = ScoreDisplay(app2.scorer, max(0,score))
    score = app3.score
    app3.run()
    print(scorer)
    print(app2.spoken.split())
game5.py
Displaying game5.py.
