import requests
import sqlite3
import os
import time

# Setup database path (always local to this script)
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "anime.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS anime (
        id INTEGER PRIMARY KEY,
        title TEXT,
        score REAL,
        members INTEGER
    )
""")

# Optional: Clear old data
cursor.execute("DELETE FROM anime")

# Prepare list to store all fetched anime
all_anime = []

# Fetch top 100 anime using pagination (25 per page × 4 pages)
for page in range(1, 5):
    url = f"https://api.jikan.moe/v4/top/anime?page={page}&limit=25"
    print(f"Fetching page {page}...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            json_data = response.json()
            if 'data' in json_data:
                anime_list = json_data['data']
                print(f"Fetched {len(anime_list)} anime from page {page}")
                all_anime.extend(anime_list)
            else:
                print(f"Page {page} response missing 'data'")
        else:
            print(f"Failed to fetch page {page}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
    
    time.sleep(1)  # Prevent rate-limiting

print(f"\nTotal anime collected: {len(all_anime)}\n")

# Insert all anime into the database
inserted = 0
for anime in all_anime:
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO anime (id, title, score, members)
            VALUES (?, ?, ?, ?)
        """, (
            anime.get('mal_id'),
            anime.get('title'),
            anime.get('score'),
            anime.get('members')
        ))
        inserted += 1
    except Exception as e:
        print(f"Error inserting anime ID {anime.get('mal_id')}: {e}")

# Commit and close
conn.commit()
conn.close()

print(f"Inserted {inserted} anime into anime.db")
