import json
import math
from datetime import datetime, timedelta
import os

R = math.pow(2, 1/16)  # ≈1.04427, for context
GOAL_TEMPO = 120
RETENTION_TARGET = 0.9

def initialize_srs_item(start, end, is_hardest=False, successful_tempo=None):
    """Create a PracticeItem with FSRS parameters."""
    difficulty = 1 - (successful_tempo / GOAL_TEMPO) if successful_tempo else (0.8 if is_hardest else 0.5)
    stability = 1.0 if is_hardest else 3.0
    return {
        "id": f"item-{start}-{end}-{datetime.now().timestamp()}",
        "piece_id": "twinkle",
        "user_id": "user1",
        "passage_start": start,
        "passage_end": end,
        "interval": stability * (1 - difficulty),
        "stability": stability,
        "difficulty": difficulty,
        "review_history": [],
        "last_scheduled": None,
        "is_hardest": is_hardest,
        "is_full_subpiece": not is_hardest,
        "successful_tempo": successful_tempo or (90 if is_hardest else 110)
    }

def add_new_item():
    """Prompt user to add a new practice item."""
    try:
        start = int(input("Enter passage start measure (e.g., 1): "))
        end = int(input("Enter passage end measure (e.g., 1): "))
        if start < 0 or end < start:
            print("Invalid: start must be non-negative, end >= start")
            return None
        is_hardest = input("Is this a hardest measure? (y/n): ").lower() == 'y'
        tempo_input = input("Enter successful tempo (BPM, press Enter for default): ")
        successful_tempo = float(tempo_input) if tempo_input else None
        if successful_tempo and not (30 <= successful_tempo <= 300):
            print("Invalid: tempo must be 30-300 BPM")
            return None
        return initialize_srs_item(start, end, is_hardest, successful_tempo)
    except ValueError:
        print("Invalid input; item not added")
        return None

def update_srs_item(item, score, current_date):
    """Update SRS parameters after review."""
    review_entry = {
        "timestamp": current_date.timestamp(),
        "score": score,
        "tempo": item["successful_tempo"]
    }
    new_history = item["review_history"] + [review_entry]
    stability = item["stability"] * (1 + 0.1 * (score - 2.5))
    stability = max(0.1, stability)
    difficulty = item["difficulty"]  # Fixed for simulation
    interval = stability * (1 - difficulty) * math.log(1 / (1 - RETENTION_TARGET))
    return {
        **item,
        "review_history": new_history,
        "stability": stability,
        "difficulty": difficulty,
        "interval": interval,
        "last_scheduled": current_date.timestamp()
    }

def generate_practice_queue(items, current_date, session_duration):
    """Generate queue for session."""
    now = current_date.timestamp()
    due_items = [
        item for item in items
        if not item["last_scheduled"] or now >= item["last_scheduled"] + item["interval"] * 86400
    ]
    new_items = [item for item in items if not item["last_scheduled"]][:2]
    prioritized = sorted(
        due_items,
        key=lambda x: (-x["is_hardest"], x["last_scheduled"] or 0)
    )
    return prioritized[:max(5, session_duration // 5)] + new_items

def save_practice_items(items, filename="practice_items.json"):
    """Save items to JSON."""
    with open(filename, "w") as f:
        json.dump(items, f, indent=2)

def load_practice_items(filename="practice_items.json"):
    """Load items from JSON."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def save_logs(logs, filename="logs.json"):
    """Save logs to JSON."""
    with open(filename, "w") as f:
        json.dump(logs, f, indent=2)

def load_logs(filename="logs.json"):
    """Load logs from JSON."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def summarize_year(items, logs):
    """Summarize simulation metrics."""
    review_count = sum(1 for log in logs if "Reviewed item" in log)
    avg_stability = sum(item["stability"] for item in items) / len(items) if items else 0
    retention_rate = sum(
        1 for item in items
        if item["review_history"] and item["review_history"][-1]["score"] >= 3
    ) / len(items) if items else 0
    return (
        f"Reviews: {review_count}, "
        f"Avg Stability: {avg_stability:.2f}, "
        f"Retention Rate: {retention_rate * 100:.1f}%"
    )

def main():
    """Run the SRS sandbox simulation."""
    items = load_practice_items()
    logs = load_logs()
    current_date = datetime(2025, 8, 20)

    # Initialize items if empty
    if not items:
        items = [
            initialize_srs_item(i, i, is_hardest=i < 5, successful_tempo=90 if i < 5 else 110)
            for i in range(10)
        ]
        save_practice_items(items)
        logs.append(f"{current_date.isoformat()}: Initialized 10 items")
        save_logs(logs)

    while True:
        print(f"\nSimulated Date: {current_date.date()}")
        print("1. Start Session")
        print("2. Add New Item")
        print("3. Advance 1 Day")
        print("4. Advance 1 Week")
        print("5. Advance to Next Due")
        print("6. Complete Year")
        print("7. Exit")
        choice = input("Choose an option (1-7): ")

        if choice == "1":
            session_duration = int(input("Session duration (minutes): ") or 30)
            queue = generate_practice_queue(items, current_date, session_duration)
            logs.append(f"{current_date.isoformat()}: Started session with {len(queue)} items")
            print("\nPractice Queue:")
            for item in queue:
                print(f"{'Hardest' if item['is_hardest'] else 'Sub-piece'} Measure {item['passage_start'] + 1}-{item['passage_end'] + 1}")
                score = input(f"Enter score (0-5) for measure {item['passage_start'] + 1}-{item['passage_end'] + 1}: ")
                try:
                    score = int(score)
                    if 0 <= score <= 5:
                        items = [
                            update_srs_item(i, score, current_date) if i["id"] == item["id"] else i
                            for i in items
                        ]
                        logs.append(
                            f"{current_date.isoformat()}: Reviewed item {item['passage_start'] + 1}-{item['passage_end'] + 1}: "
                            f"score={score}, interval={items[-1]['interval']:.2f}, stability={items[-1]['stability']:.2f}"
                        )
                    else:
                        print("Score must be 0-5")
                except ValueError:
                    print("Invalid input; skipping")
            save_practice_items(items)
            save_logs(logs)

        elif choice == "2":
            new_item = add_new_item()
            if new_item:
                items.append(new_item)
                save_practice_items(items)
                logs.append(f"{current_date.isoformat()}: Added item measure {new_item['passage_start'] + 1}-{new_item['passage_end'] + 1}")
                save_logs(logs)
                print(f"Added item: {'Hardest' if new_item['is_hardest'] else 'Sub-piece'} Measure {new_item['passage_start'] + 1}-{new_item['passage_end'] + 1}")

        elif choice in ["3", "4", "5", "6"]:
            days = {
                "3": 1,
                "4": 7,
                "6": 365 - (current_date - datetime(2025, 8, 20)).days
            }.get(choice, 0)
            if choice == "5":
                due_dates = [
                    i["last_scheduled"] + i["interval"] * 86400
                    for i in items if i["last_scheduled"]
                ]
                if due_dates:
                    next_due = min(due_dates)
                    if next_due > current_date.timestamp():
                        days = (next_due - current_date.timestamp()) / 86400
            current_date += timedelta(days=days)
            logs.append(f"{current_date.isoformat()}: Advanced time by {days:.1f} days")
            save_logs(logs)

        elif choice == "7":
            break

        print("\nCurrent Items:")
        for item in items:
            due = "Now" if not item["last_scheduled"] else datetime.fromtimestamp(
                item["last_scheduled"] + item["interval"] * 86400
            ).date()
            print(
                f"{'Hardest' if item['is_hardest'] else 'Sub-piece'} Measure {item['passage_start'] + 1}-{item['passage_end'] + 1}: "
                f"Due={due}, Stability={item['stability']:.2f}"
            )
        print("\nSummary:", summarize_year(items, logs))
        print("\nLogs (last 5):")
        for log in logs[-5:]:
            print(log)

if __name__ == "__main__":
    main()