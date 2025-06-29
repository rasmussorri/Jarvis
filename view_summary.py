import json
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python view_summary.py <monthly_report.json>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        data = json.load(f)

    year = data.get("year", "Unknown")
    month = data.get("month", "Unknown")
    summary = data.get("summary", "")

    print(f"\n📅 Monthly Report: {year}-{str(month).zfill(2)}\n")
    print("📝 Summary:\n")

    # Clean up the summary text by removing extra newlines and spaces
    summary = summary.replace('\n\n', ' ').replace('\n', ' ').strip()
    
    # Split on periods followed by spaces for sentences
    sentences = summary.split('. ')
    for s in sentences:
        if s.strip():
            # Remove trailing period if it exists and add it back
            sentence = s.strip().rstrip('.')
            print(f"- {sentence}.")
    print()

if __name__ == "__main__":
    main()
