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
        
    def transcribe_and_input(self, filename='recorded_audio'):
        audio = record_audio(filename=filename)
        isValid, transcription = self.asrCodingModel.transcribe(filename)
        
        if not isValid:
            print("Invalid transcription.")
            return
        
        # Select text area
        if self.text_area != self.driver.find_element(By.CSS_SELECTOR, ".ace_text-input"):
            self.text_area = self.driver.find_element(By.CSS_SELECTOR, ".ace_content")
            self.text_area.click()
            self.text_area = self.driver.find_element(By.CSS_SELECTOR, ".ace_text-input")
        
        for line in transcription.split('\n'):
            self.text_area.send_keys(Keys.RETURN)
            if line == "[indent]":
                self.text_area.send_keys(Keys.TAB)
            elif line == "[unindent]":
                self.text_area.send_keys(Keys.SHIFT, Keys.TAB)
            elif line == "[backspace]":
                self.text_area.send_keys(Keys.BACKSPACE)
            else:
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
        command = input("Enter command (record, run, stop): ").strip().lower()
        if command == 'record':
            ide.transcribe_and_input()
        elif command == 'run':
            ide.run_program()
        elif command == 'stop':
            ide.close_browser()
            break
        else:
            print("Unknown command. Please enter 'record', 'run', or 'stop'.")

def main():
    ide = KarelIDE()
    command_loop(ide)

if __name__ == '__main__':
    main()
