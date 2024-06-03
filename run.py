from model import *
from audio import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


import time

def main():
    asrCodingModel = ASRCodingModel()

    filename='recorded_audio'

    audio = record_audio(filename=filename)
    isValid, transcription = asrCodingModel.transcribe(filename)
    
    print(transcription)

    if not isValid:
        return
    
    # Load Karel editor
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://compedu.stanford.edu/karel-reader/docs/python/en/ide.html")
    time.sleep(5)


    # Click on the text area to activate it, then swap to text-input
    text_area = driver.find_element(By.CSS_SELECTOR, ".ace_content")
    text_area.click()
    text_area = driver.find_element(By.CSS_SELECTOR, ".ace_text-input")

    # Type the text you want to add to the IDE
    transcription = "move()\nmove()\nmove()"

    # Enter in each line separately and wait
    for line in transcription.split('\n'):
        text_area.send_keys(Keys.RETURN)
        text_area.send_keys(line)
        time.sleep(1)

    time.sleep(2)

    # Run the program
    run_button = driver.find_element(By.ID, "ideRunButton")
    run_button.click()

    # Close the browser after 10 seconds
    time.sleep(10) 
    driver.quit()
    


if __name__ == '__main__':
    main()