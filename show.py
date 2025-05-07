import sqlite3
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "anime.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Top 5 by score
print("Top 5 by Score")
print("=" * 60)
cursor.execute("SELECT title, score FROM anime ORDER BY score DESC LIMIT 5")
for row in cursor.fetchall():
    print(f"Title: {row[0]} | Score: {row[1]}")
print()

# Top 5 by members
print("Top 5 by Popularity (Members)")
print("=" * 60)
cursor.execute("SELECT title, members FROM anime ORDER BY members DESC LIMIT 5")
for row in cursor.fetchall():
    print(f"Title: {row[0]} | Members: {row[1]}")
print()

conn.close()