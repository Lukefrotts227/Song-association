import os 
import tkinter as tk 
from tkinter import *
import customtkinter
import random
import time 

import pygame as pg
import wave
import pyaudio
from threading import Thread

scores = {}
PATH = "output3.wav"


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
            self.stop()

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


def main():
    pg.init()
    screen = pg.display.set_mode((640, 480))
    font = pg.font.Font(None, 40)
    gray = pg.Color('gray19')
    blue = pg.Color('dodgerblue')
    clock = pg.time.Clock()
    timer = 10
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
            timer = 10

        screen.fill(gray)
        txt = font.render(str(round(timer, 2)), True, blue)
        screen.blit(txt, (70, 70))
        pg.display.flip()
        dt = clock.tick(30) / 1000

    audio.stop_recording()
    pg.quit()


if __name__ == '__main__':
    main()
