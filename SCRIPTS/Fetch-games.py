import requests
import time
import json

def safe_get_json(url, max_retries=3, delay=2):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                try:
                    return response.json()
                except ValueError:
                    print(f"[Attempt {attempt}] Invalid JSON.")
            else:
                print(f"[Attempt {attempt}] Error {response.status_code}")
        except requests.RequestException as e:
            print(f"[Attempt {attempt}] Request failed: {e}")
        time.sleep(delay * attempt)
    return None

# Step 1: Get all archive URLs
username = "MagnusCarlsen"
url = f"https://api.chess.com/pub/player/{username}/games/archives"
data = safe_get_json(url)
archives = data["archives"]
print(f" Total months: {len(archives)}")

# Step 2: Loop through and download all games
all_games = []
for i, archive_url in enumerate(archives):
    month_data = safe_get_json(archive_url)
    if month_data and "games" in month_data:
        all_games.extend(month_data["games"])
        print(f"Month {i+1}/{len(archives)} done — {len(month_data['games'])} games")
    time.sleep(0.3)

print(f"\n Total games downloaded: {len(all_games)}")

# Step 3: Save immediately
with open("magnus_all_games.json", "w") as f:
    json.dump(all_games, f)
print("Saved to magnus_all_games.json")
