import speech_recognition as sr
import json
import os
from datetime import date
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# File Management
def get_today_filename():
    today_str = date.today().isoformat()
    return f"logs/{today_str}.json"

def ask_questions():
    questions = [
        "How was your day?",
        "What did you accomplish?",
        "How did you feel?"
    ]
    answers = {}
    for question in questions:
        answer = input(f"{question} ")
        answers[question] = answer
    return answers

def save_entry(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    filename = get_today_filename()
    if os.path.exists(filename):
        print(f"⚠️  Entry for today already exists: {filename}")
        overwrite = input("Do you want to overwrite it? (y/n): ").lower()
        if overwrite != 'y':
            print("Aborting.")
            return

    answers = ask_questions()
    entry = {
        "date": date.today().isoformat(),
        "responses": answers
    }
    save_entry(entry, filename)
    print(f"✅ Entry saved to {filename}")

# STT - Speech to Text
def listen_and_transcribe():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Say something! I'm listening...")
        audio = recognizer.listen(source)

    try:
        print("🔍 Transcribing...")
        text = recognizer.recognize_google(audio)
        print("🧠 You said:", text)
    except sr.UnknownValueError:
        print("😵 I have no idea what you just said.")
    except sr.RequestError as e:
        print(f"🚨 Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    main()
