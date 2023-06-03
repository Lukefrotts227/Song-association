import wave 
import pyaudio
from threading import Thread 
import time



import wave
import pyaudio
from threading import Thread

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
            if self.stream:
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




          