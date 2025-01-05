from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from twilio.rest import Client
import os

# Load environment variables from .env file
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
RECIPIENT_PHONE_NUMBER = os.getenv('RECIPIENT_PHONE_NUMBER')

def get_word_of_the_day():
    # Set up Selenium WebDriver
    service = Service('path_to_your_chromedriver')  # Replace with the path to your ChromeDriver
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.merriam-webster.com/word-of-the-day")

    try:
        # Extract the word of the day and its definition
        word = driver.find_element(By.CSS_SELECTOR, ".word-and-pronunciation h1").text
        definition = driver.find_element(By.CSS_SELECTOR, ".wod-definition-container p").text
    except Exception as e:
        print(f"Error extracting data: {e}")
        word, definition = None, None
    finally:
        driver.quit()

    return word, definition

def send_text_message(word, definition):
    if not word or not definition:
        print("No word or definition to send.")
        return

    message_body = f"Word of the Day: {word}\nDefinition: {definition}"

    # Set up Twilio client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=RECIPIENT_PHONE_NUMBER
        )
        print(f"Message sent: SID {message.sid}")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    word, definition = get_word_of_the_day()
    send_text_message(word, definition)
