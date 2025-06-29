import speech_recognition as sr
import json
import os
import sys
from datetime import date, datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Init OpenAI
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    print("❌ Warning: OPENAI_API_KEY not found in .env file")

### Utility
def get_today_filename():
    today_str = date.today().isoformat()
    return f"logs/{today_str}.json"

def ensure_logs_folder():
    if not os.path.exists("logs"):
        os.makedirs("logs")

### Daily Logging
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

def daily_mode():
    ensure_logs_folder()
    filename = get_today_filename()

    existing = None
    if os.path.exists(filename):
        with open(filename) as f:
            existing = json.load(f)
        print("⚠️  Entry for today already exists:")
        for q, a in existing.get("responses", {}).items():
            print(f"- {q}: {a}")
        overwrite = input("Do you want to overwrite it? (y/n): ").lower()
        if overwrite != 'y':
            print("Aborting.")
            return

    answers = ask_questions()
    entry = {
        "date": date.today().isoformat(),
        "responses": answers
    }
    with open(filename, 'w') as f:
        json.dump(entry, f, indent=2)
    print(f"✅ Entry saved to {filename}")

### Monthly Summarizer
def load_logs_for_month(year, month):
    logs = []
    for filename in os.listdir("logs"):
        if filename.endswith(".json"):
            path = os.path.join("logs", filename)
            with open(path) as f:
                data = json.load(f)
                try:
                    log_date = datetime.strptime(data["date"], "%Y-%m-%d")
                    if log_date.year == year and log_date.month == month:
                        logs.append(data)
                except Exception as e:
                    print(f"⚠️ Skipping {filename}: {e}")
    logs.sort(key=lambda x: x["date"])
    return logs

def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def summarize_batch(batch, batch_num):
    print(f"🧩 Summarizing batch {batch_num} with {len(batch)} entries...")
    batch_prompt = (
        f"You are an assistant summarizing a batch of daily diary entries.\n\n"
        f"Please read ALL entries below and write a concise summary in 3-5 sentences, capturing main events, emotions, and themes.\n\n"
        f"ENTRIES:\n\n"
    )

    for day in batch:
        batch_prompt += f"Date: {day['date']}\n"
        for q, a in day["responses"].items():
            batch_prompt += f"{q}: {a}\n"
        batch_prompt += "\n"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who summarizes diary reflections."},
            {"role": "user", "content": batch_prompt}
        ]
    )
    return response.choices[0].message.content

def extract_bullets_for_day(day):
    day_prompt = (
        f"You're an assistant helping summarize diary entries for later monthly reflection.\n\n"
        f"Please extract 3 clear bullet points summarizing this day's diary entry. Focus on main events, emotional state, and any reflections.\n\n"
        f"ENTRY:\n"
        f"Date: {day['date']}\n"
    )
    for q, a in day["responses"].items():
        day_prompt += f"{q}: {a}\n"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who writes concise bullet points."},
            {"role": "user", "content": day_prompt}
        ]
    )
    return response.choices[0].message.content

def extract_bullets_for_day(day):
    day_prompt = (
        "You are a helpful assistant summarizing a single day's diary entry for later monthly reflection.\n\n"
        "Extract exactly 3 clear, short bullet points that capture:\n"
        "- Main events or activities\n"
        "- Emotional state\n"
        "- Reflections or insights\n\n"
        f"ENTRY (Date: {day['date']}):\n"
    )
    for q, a in day["responses"].items():
        day_prompt += f"{q}: {a}\n"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant who writes concise bullet points for diaries."},
            {"role": "user", "content": day_prompt}
        ]
    )
    return response.choices[0].message.content


def generate_monthly_summary(all_responses):
    if not client:
        print("❌ OpenAI client not available. Check your .env file and API key.")
        return None

    try:
        print("🪄 Step 1: Extracting bullet points for each day...")
        bullet_points_list = []
        for day in all_responses:
            bullets = extract_bullets_for_day(day)
            numbered_bullets = f"Date: {day['date']}\n{bullets.strip()}\n"
            bullet_points_list.append(numbered_bullets)

        print("✅ Bullet points extracted for all days.\n")

        print("🪄 Step 2: Building FINAL summarization prompt...")
        final_prompt = (
            "You are an assistant creating a single monthly diary reflection from these 30 days of bullet-point summaries.\n\n"
            "Instructions:\n"
            "- Analyze ALL 30 days EQUALLY.\n"
            "- Identify repeated themes and emotional trends.\n"
            "- Cover early, middle, and late month.\n"
            "- Write 5-8 sentences summarizing the entire month.\n"
            "- Be personal, empathetic, and reflective.\n"
            "- Do NOT focus only on the last days.\n"
            "- Include patterns that emerge over time.\n\n"
            "DAILY BULLET POINTS (NUMBERED):\n\n"
        )

        for i, bullets in enumerate(bullet_points_list, start=1):
            final_prompt += f"{i}. {bullets}\n\n"

        print("✅ Prompt ready. Calling GPT...\n")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who writes monthly diary reflections."},
                {"role": "user", "content": final_prompt}
            ]
        )

        print("✅ Monthly summary generated!\n")
        return response.choices[0].message.content

    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return None




def monthly_mode():
    ensure_logs_folder()
    year = int(input("Enter year (e.g. 2025): "))
    month = int(input("Enter month (1-12): "))

    logs = load_logs_for_month(year, month)
    if not logs:
        print("❌ No logs found for that month.")
        return

    print(f"✅ Loaded {len(logs)} daily entries.")
    summary = generate_monthly_summary(logs)
    if summary:
        report_filename = f"monthly_report_{year}-{month:02}.json"
        with open(report_filename, 'w') as f:
            json.dump({"year": year, "month": month, "summary": summary}, f, indent=2)
        print(f"✅ Monthly summary saved to {report_filename}")
    else:
        print("❌ Failed to generate summary.")

### Main Entrypoint
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [daily|monthly]")
        return

    mode = sys.argv[1].lower()
    if mode == "daily":
        daily_mode()
    elif mode == "monthly":
        monthly_mode()
    else:
        print(f"Unknown mode: {mode}")

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