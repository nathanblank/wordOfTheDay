from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
from twilio.rest import Client
import os

# Load environment variables from .env file
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
RECIPIENT_PHONE_NUMBER = os.getenv('RECIPIENT_PHONE_NUMBER')
RECIPIENT_PHONE_NUMBER2 = os.getenv('RECIPIENT_PHONE_NUMBER2')

from datetime import datetime

# Get the current date
current_date = datetime.now()

# Format the date as MM-DD-YYYY
formatted_date = current_date.strftime("%m-%d-%Y")



# Set up Selenium WebDriver
driver = webdriver.Chrome()
driver.set_page_load_timeout(10)  # Timeout after 10 seconds




def get_word_of_the_day():
    try:
             
        try:
            # Attempt to load the page
            driver.get("https://www.merriam-webster.com/word-of-the-day")
        except TimeoutException:
            print("Page load timed out. Stopping the page load.")
            driver.execute_script("window.stop();")  # Stop further loading
        # Extract the word of the day and its definition
        word = driver.find_element(By.CLASS_NAME,"word-header-txt").text.capitalize()
        attributes = driver.find_element(By.CLASS_NAME, "word-attributes").text.split(" ")
        definition = driver.find_elements(By.TAG_NAME, "p")[0].text
        description =  driver.find_elements(By.TAG_NAME, "p")[1].text[3:]
    except Exception as e:
        print(f"Error extracting data: {e}")
        word, definition, description, attributes = None, None, None
    finally:
        driver.quit()

    return word, definition, description, attributes

def send_text_message(word, definition, description, attributes):
    if not word or not definition or not description or not attributes:
        print("No word or definition to send.")
        return
    partOfSpeech = attributes[0].capitalize()
    message_body = f"{formatted_date}\nWord of the Day: {word} ({attributes[1]})\n\nPart of speech: {partOfSpeech}\n\nDefinition: {definition}\n\nExample: {description}"

    # Set up Twilio client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=RECIPIENT_PHONE_NUMBER
        )
        print(f"Message sent: SID {message.sid}")
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=RECIPIENT_PHONE_NUMBER2
        )
        print(f"Message sent: SID {message.sid}")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    word, definition, description, attributes = get_word_of_the_day()
    print()
    send_text_message(word, definition, description, attributes)
