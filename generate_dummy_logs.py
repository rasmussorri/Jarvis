import os
import json
from datetime import date, timedelta

if not os.path.exists("logs"):
    os.makedirs("logs")

start_date = date(2025, 6, 1)
end_date = date(2025, 6, 30)
delta = timedelta(days=1)

entries = [
    {
        "How was your day?": "It started out sunny so I went for a walk, but in the afternoon I felt really drained from work meetings. In the evening I read a bit and tried to relax.",
        "What did you accomplish?": "Managed to clear my inbox and set up two important client calls for next week.",
        "How did you feel?": "A bit anxious but relieved to have things planned. Ended the day feeling okay."
    },
    {
        "How was your day?": "Today was really hectic. Meetings back to back with barely any time to eat lunch. I felt rushed all day.",
        "What did you accomplish?": "Wrapped up the quarterly report and sent it out just before the deadline.",
        "How did you feel?": "Exhausted and a little proud I got it done."
    },
    {
        "How was your day?": "Had a slower morning. Spent some time journaling and making coffee. Work was pretty easygoing.",
        "What did you accomplish?": "Finished some minor bug fixes and reviewed a coworker’s PR.",
        "How did you feel?": "Calm and grateful for a light day."
    },
    {
        "How was your day?": "It was gloomy outside which matched my mood. Felt unmotivated and distracted all day.",
        "What did you accomplish?": "Managed to get through emails and organize my task list, but not much else.",
        "How did you feel?": "Frustrated with myself but trying to accept it."
    },
    {
        "How was your day?": "Busy but productive. Went for a run before work which helped a lot.",
        "What did you accomplish?": "Had a solid planning meeting with the team and knocked out a big feature.",
        "How did you feel?": "Focused and positive for most of the day."
    },
    {
        "How was your day?": "Woke up late and felt behind from the start. Work was okay but I never really caught up.",
        "What did you accomplish?": "Got some small tasks done and helped a teammate debug.",
        "How did you feel?": "Stressed and annoyed at myself."
    },
    {
        "How was your day?": "Had the day off! Slept in and then went to the park. Ate ice cream and read for a while.",
        "What did you accomplish?": "Relaxed intentionally, no work at all.",
        "How did you feel?": "Happy, free, a little nostalgic."
    },
    {
        "How was your day?": "Lots of errands. Bank, groceries, cleaned the apartment.",
        "What did you accomplish?": "Got the place looking great and stocked up on food.",
        "How did you feel?": "Productive but physically tired."
    },
    {
        "How was your day?": "Worked from a coffee shop for a change of scenery. Felt good to be around people.",
        "What did you accomplish?": "Cleared out bug tickets and had a good design review.",
        "How did you feel?": "Refreshed and more social than usual."
    },
    {
        "How was your day?": "Super social. Lunch with a friend, then a family call in the evening.",
        "What did you accomplish?": "No real work tasks, but stayed connected with important people.",
        "How did you feel?": "Warm, supported, slightly drained from so much talking."
    },
    # Repeat as needed with variations
]

current_date = start_date
i = 0
while current_date <= end_date:
    data = {
        "date": current_date.isoformat(),
        "responses": entries[i % len(entries)]
    }
    filename = f"logs/{current_date.isoformat()}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Created {filename}")
    current_date += delta
    i += 1

print("\n🎉 Done generating 30 *richer* dummy logs!")
