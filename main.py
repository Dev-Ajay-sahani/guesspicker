import requests
import time
import random
import os
from threading import Thread
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Config
TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "1380950004667252786")
LOW = 250000
HIGH = 500000
MIN_DELAY = 1.6
MAX_DELAY = 1.7

# Flask app
app = Flask(__name__)

# Discord headers
headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

# Send message to Discord channel
def send_message(channel_id, content):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    payload = {"content": content}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"❌ Error {response.status_code}: {response.text}")
    else:
        print(f"✅ Sent guess: {content}")

# Loop to keep guessing
def guess_loop():
    all_numbers = list(range(LOW + 1, HIGH))
    guessed = set()
    while True:
        random.shuffle(all_numbers)
        for guess in all_numbers:
            if guess in guessed or guess + 1 in guessed or guess - 1 in guessed:
                continue
            guessed.update({guess, guess + 1, guess - 1})
            send_message(CHANNEL_ID, str(guess))
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            send_message(CHANNEL_ID, str(guess + 1))
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            send_message(CHANNEL_ID, str(guess - 1))
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

# Start background thread only once
started = False

@app.before_request
def start_thread_once():
    global started
    if not started:
        started = True
        t = Thread(target=guess_loop)
        t.daemon = True
        t.start()

# Root route
@app.route('/')
def home():
    return "Guesser Bot is running."

# Run app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
