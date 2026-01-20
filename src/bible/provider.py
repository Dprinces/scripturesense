import sqlite3
import logging
import os

class BibleProvider:
    def __init__(self, db_path="data/bible.db"):
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
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
        
        # Seed if empty
        cursor.execute("SELECT count(*) FROM verses")
        if cursor.fetchone()[0] == 0:
            self._seed_demo_data(cursor)
            
        conn.commit()
        conn.close()

    def _seed_demo_data(self, cursor):
        logging.info("Seeding demo Bible data...")
        verses = [
            ("John", 3, 16, "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.", "KJV"),
            ("Genesis", 1, 1, "In the beginning God created the heaven and the earth.", "KJV"),
            ("Psalm", 23, 1, "The LORD is my shepherd; I shall not want.", "KJV"),
            ("Romans", 8, 1, "There is therefore now no condemnation to them which are in Christ Jesus, who walk not after the flesh, but after the Spirit.", "KJV"),
            ("1 Corinthians", 13, 4, "Charity suffereth long, and is kind; charity envieth not; charity vaunteth not itself, is not puffed up,", "KJV")
        ]
        cursor.executemany("INSERT INTO verses (book, chapter, verse, text, translation) VALUES (?, ?, ?, ?, ?)", verses)

    def get_verse(self, book, chapter, verse, translation="KJV"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simple exact match for now
        # Note: Book names must match exactly what is in DB.
        # The detector returns standard names (e.g., "1 Corinthians"), ensure DB matches.
        
        # Handle "Psalms" vs "Psalm"
        if book == "Psalms":
            book = "Psalm" # Common KJV convention often uses singular for the book title in some DBs, or plural. My seed used "Psalm" for 23:1 but usually it's "Psalms". Let's fix seed to be standard if needed. Actually standard is "Psalms", but individual is "Psalm". I'll query for both just in case or rely on seed.
            # Let's just try strict first.
            
        cursor.execute('''
            SELECT text FROM verses 
            WHERE book = ? AND chapter = ? AND verse = ? AND translation = ?
        ''', (book, chapter, verse, translation))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        return None
