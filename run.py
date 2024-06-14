from model import *
from audio import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

class KarelIDE:
    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get("https://compedu.stanford.edu/karel-reader/docs/python/en/ide.html")
        time.sleep(5)
        self.asrCodingModel = ASRCodingModel()
        self.text_area = None
    
    def transcribe_sample(self, filename='recorded_audio', type="standard"):

        isValid, transcription = self.asrCodingModel.transcribe(filename)
        
        if not isValid:
            print("Invalid transcription.")
            return
        
        # Select text area
        self.text_area = self.driver.find_element(By.CSS_SELECTOR, ".ace_content")
        self.text_area.click()
        self.text_area = self.driver.find_element(By.CSS_SELECTOR, ".ace_text-input")

        for i in range(100):
            self.text_area.send_keys(Keys.DOWN)
        
        for line in transcription.split('\n'):

            # Check for Run or Reset Commands
            if line == "[run]" or line == "[reset]":
                self.run_program()
                break

            
            if line == "[indent]":
                self.text_area.send_keys(Keys.TAB)
            elif line == "[unindent]":
                self.text_area.send_keys(Keys.SHIFT, Keys.TAB)
            elif line == "[backspace]":
                self.text_area.send_keys(Keys.BACKSPACE)
            elif line == "[return]":
                self.text_area.send_keys(Keys.RETURN)
            else:
                self.text_area.send_keys(Keys.RETURN)
                self.text_area.send_keys(line)
                
            time.sleep(1)
        
        print("Transcription inputted to IDE.")
        
    def transcribe_and_input(self, filename='recorded_audio', type="standard"):

        duration = 10 if type == "standard" else 3
        audio = record_audio(filename=filename, duration=duration)
        isValid, transcription = self.asrCodingModel.transcribe(filename)
        
        if not isValid:
            print("Invalid transcription.")
            return
        
        # Select text area
        self.text_area = self.driver.find_element(By.CSS_SELECTOR, ".ace_content")
        self.text_area.click()
        self.text_area = self.driver.find_element(By.CSS_SELECTOR, ".ace_text-input")

        for i in range(100):
            self.text_area.send_keys(Keys.DOWN)
        
        for line in transcription.split('\n'):

            # Check for Run or Reset Commands
            if line == "[run]" or line == "[reset]":
                self.run_program()
                break

            
            if line == "[indent]":
                self.text_area.send_keys(Keys.TAB)
            elif line == "[unindent]":
                self.text_area.send_keys(Keys.SHIFT, Keys.TAB)
            elif line == "[backspace]":
                self.text_area.send_keys(Keys.BACKSPACE)
            elif line == "[return]":
                self.text_area.send_keys(Keys.RETURN)
            else:
                self.text_area.send_keys(Keys.RETURN)
                self.text_area.send_keys(line)
                
            time.sleep(1)
        
        print("Transcription inputted to IDE.")
    
    def run_program(self):
        run_button = self.driver.find_element(By.ID, "ideRunButton")
        run_button.click()
        print("Program is running...")
        
    def close_browser(self):
        self.driver.quit()
        print("Browser closed.")
        
def command_loop(ide):
    while True:
        command = input("Enter command (record, record_continuous, run_sample, run, stop): ").strip().lower()
        if command == 'record':
            ide.transcribe_and_input()
        elif command == 'record_continuous':
            while True:
                ide.transcribe_and_input(type="continuous")
        elif command == 'run':
            ide.run_program()
        elif command == 'stop':
            ide.close_browser()
            break
        elif command == 'run_sample':
            ide.transcribe_sample(filename='./audio_files/CS_224S_CM_ElevenLabs_Example_26.wav', type="standard")
            ide.run_program()
        else:
            print("Unknown command. Please enter 'record', 'record_continuous','run_sample', 'run', or 'stop'.")

def main():
    ide = KarelIDE()
    command_loop(ide)

if __name__ == '__main__':
    main()
