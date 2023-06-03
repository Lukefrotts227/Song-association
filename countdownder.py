import time
import datetime


class countDown:

    def __init__(self, seconds): 
        self.seconds = seconds 
    

    def start(self):
        
        secs = self.seconds
        while secs > 0:
            timer = f"{secs} seconds"
            
            time.sleep(1)
            self.seconds-1
            secs -= 1


