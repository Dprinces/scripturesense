import re
import logging
from .books import BIBLE_BOOKS, BOOK_VARIATIONS

class ScriptureDetector:
    def __init__(self):
        self.books = BIBLE_BOOKS
        self.book_pattern = self._build_book_pattern()

    def _build_book_pattern(self):
        all_books = sorted(self.books + list(BOOK_VARIATIONS.keys()), key=len, reverse=True)
        escaped_books = [re.escape(b) for b in all_books]
        return "|".join(escaped_books)

    def _normalize_text(self, text):
        text = text.lower()
        replacements = {
            "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
            "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
            "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14", "fifteen": "15",
            "sixteen": "16", "seventeen": "17", "eighteen": "18", "nineteen": "19", "twenty": "20",
            "thirty": "30", "forty": "40", "fifty": "50",
            "first": "1st", "second": "2nd", "third": "3rd"
        }
        for word, digit in replacements.items():
            text = re.sub(r'\b' + word + r'\b', digit, text)
        return text

    def detect(self, text):
        if not text:
            return []

        normalized_text = self._normalize_text(text)
        
        # Pattern: Book + (optional "chapter") + Number + (optional "verse" or ":") + Number
        pattern = fr"\b({self.book_pattern})\b\s*(?:chapter\s*)?(\d+)\s*(?::|verse\s*|\s+)?\s*(\d+)"
        
        matches = re.findall(pattern, normalized_text, re.IGNORECASE)
        results = []
        
        for match in matches:
            book_raw, chapter, verse = match
            book_std = self._get_standard_book_name(book_raw)
            
            if book_std:
                # Mock Confidence Scoring
                # Regex is deterministic, so it's usually high.
                # We can penalize if the spoken text was very noisy or long compared to the match.
                # For now, let's assign a static high confidence for clear matches.
                confidence = 0.95 
                
                results.append({
                    "book": book_std,
                    "chapter": int(chapter),
                    "verse": int(verse),
                    "confidence": confidence
                })
                logging.info(f"Detected: {book_std} {chapter}:{verse} (Conf: {confidence})")

        return results

    def _get_standard_book_name(self, raw_name):
        raw_lower = raw_name.lower()
        if raw_lower in BOOK_VARIATIONS:
            return BOOK_VARIATIONS[raw_lower]
        for book in self.books:
            if book.lower() == raw_lower:
                return book
        return None
