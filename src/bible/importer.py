import sqlite3
import logging
import os
import requests
import json

# URL for a public domain KJV SQL/JSON source or similar.
# For this task, we'll download a raw JSON/XML/CSV of the KJV Bible 
# and parse it into our SQLite DB.
# Using a reliable raw text source.

KJV_JSON_URL = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json"

class BibleImporter:
    def __init__(self, db_path="data/bible.db"):
        self.db_path = db_path

    def import_kjv(self):
        logging.info("Downloading KJV Bible...")
        try:
            response = requests.get(KJV_JSON_URL)
            response.raise_for_status()
            # Handle BOM if present
            response.encoding = 'utf-8-sig'
            data = response.json()
        except Exception as e:
            logging.error(f"Failed to download Bible data: {e}")
            return False

        logging.info("Importing KJV into database...")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Ensure table exists (it should from provider.py, but safe to check)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS verses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book TEXT,
                chapter INTEGER,
                verse INTEGER,
                text TEXT,
                translation TEXT
            )
        ''')
        
        # Clear existing KJV to avoid duplicates? Or just insert if not exists?
        # Let's clear KJV for a clean import.
        cursor.execute("DELETE FROM verses WHERE translation = 'KJV'")
        
        count = 0
        batch = []
        
        # Structure of source JSON is typically list of books -> chapters -> verses
        # Source format: [{'name': 'Genesis', 'abbrev': 'gn', 'chapters': [['In the beginning...', ...], ...]}, ...]
        
        for book_data in data:
            book_name = book_data['name']
            chapters = book_data['chapters']
            
            for ch_idx, chapter in enumerate(chapters):
                ch_num = ch_idx + 1
                for v_idx, text in enumerate(chapter):
                    v_num = v_idx + 1
                    batch.append((book_name, ch_num, v_num, text, 'KJV'))
                    
                    if len(batch) >= 1000:
                        cursor.executemany("INSERT INTO verses (book, chapter, verse, text, translation) VALUES (?, ?, ?, ?, ?)", batch)
                        batch = []
                        
            count += 1
            
        if batch:
             cursor.executemany("INSERT INTO verses (book, chapter, verse, text, translation) VALUES (?, ?, ?, ?, ?)", batch)
             
        conn.commit()
        conn.close()
        logging.info(f"Imported KJV successfully.")
        return True

if __name__ == "__main__":
    # Configure logging if run directly
    logging.basicConfig(level=logging.INFO)
    importer = BibleImporter()
    importer.import_kjv()
