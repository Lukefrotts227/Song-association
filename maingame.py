import os 
import tkinter as tk 
from tkinter import *
import customtkinter as ctk 
import random
import time 

import pygame as pg
import wave
import pyaudio
from threading import Thread

scores = {}
PATH = "output3.wav"




ctk.set_appearance_mode("System")

ctk.set_default_color_theme("green") 

class App(ctk.CTk):
    timeinsecs = 10
# Layout of the GUI will be written in the init itself
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
# Sets the title of our window to "App"
        self.title("App")   
# Dimensions of the window will be 200x200
        self.geometry("700x200") 
        
        self.timerchoice = 12

        self.generateButton = ctk.CTkButton(self, text="Exit Button", command=self.exitStage, font=("Arial", 12))
        self.generateButton.grid(row=0, column=0, columnspan=3, pady=10, padx=20, sticky="ew")

        self.time10Button = ctk.CTkButton(self, text="10 seconds", command=self.changeTime10, font=("Arial", 10))
        self.time10Button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.time20Button = ctk.CTkButton(self, text="20 seconds", command=self.changeTime20, font=("Arial", 10))
        self.time20Button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.time25Button = ctk.CTkButton(self, text="25 seconds", command=self.changeTime25, font=("Arial", 10))
        self.time25Button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # Adding some styling to the buttons

        self.grid_rowconfigure(0, weight=1)  # Make the first row expand vertically
        self.grid_columnconfigure(0, weight=1)  # Make the first column expand horizontally
        self.grid_columnconfigure(1, weight=1)  # Make the second column expand horizontally
        self.grid_columnconfigure(2, weight=1)  # Make the third column expand horizontally


    
    def exitStage(self): 
        self.destroy()

    def getTime(self): 
        return self.timerchoice
    
    def changeTime10(self): 
        App.timeinsecs = 10
    def changeTime20(self): 
        App.timeinsecs = 20
    def changeTime25(self): 
        App.timeinsecs = 25

class AudioFile:
    def __init__(self, filename):
        self.filename = filename
        self.seconds = 0
        self.timer_event = None
        self.recording_thread = None
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            print("Recording stopped...")
            wf = wave.open(self.filename, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            print("Recording saved as output3.wav")
            #self.stop()

    def start_recording(self):
        self.is_recording = True
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.frames = []
        print("Recording started...")

    def record_audio(self):
        self.start_recording()
        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)

    def start_recording_thread(self):
        self.recording_thread = Thread(target=self.record_audio)
        self.recording_thread.start()

app = App()


def main():
    pg.init()
    screen = pg.display.set_mode((640, 480))
    font = pg.font.Font(None, 40)
    gray = pg.Color('gray19')
    blue = pg.Color('dodgerblue')
    clock = pg.time.Clock()
    timer = App.timeinsecs
    
    
    dt = 0
    done = False

    audio = AudioFile(PATH)
    audio.start_recording_thread()

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        timer -= dt
        if timer <= 0:
            done = True

        screen.fill(gray)
        txt = font.render(str(round(timer, 2)), True, blue)
        screen.blit(txt, (70, 70))
        pg.display.flip()
        dt = clock.tick(30) / 1000

    audio.stop_recording()
    pg.quit()


if __name__ == '__main__':
    # Runs the app
    

    app.mainloop() 
    main()
