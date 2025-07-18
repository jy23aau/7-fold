import json
import random
import sys

# Templates for direct and meditative questions
MEDITATIVE_TEMPLATES = [
    "Reflect on this: What does {verse_summary} reveal about God's character?",
    "Think deeper: How can {verse_summary} guide your spiritual walk today?",
    "What lesson does {verse_summary} hold that aligns with {linked_verse}?",
    "Compare {verse_summary} with {linked_verse}: What truth stands out?"
]

def load_bible(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def get_chapter_verses(bible_data, book, chapter):
    try:
        book_data = next(b for b in bible_data if b['name'].lower() == book.lower())
        chapter_verses = book_data['chapters'][int(chapter)-1]
        return chapter_verses
    except Exception as e:
        print("[ERROR] Could not find chapter:", e)
        return []

def generate_direct_questions(verses):
    questions = []
    # 2 fill-in-the-blank or true/false
    for _ in range(2):
        verse = random.choice(verses)
        text = verse.strip()
        if len(text.split()) > 5:
            blanked = text.replace(random.choice(text.split()), "____", 1)
            questions.append(f"🦠 Fill in the blank: {blanked}")
        else:
            questions.append(f"🦠 True or False: {text}")
    
    # 1 Match-the-Following (fixed sample)
    questions.append("🦠 Match the Following – Match the character or action with the spiritual theme:\n\n"
                     "A (Person/Act)        B (Spiritual Theme)\n"
                     "1. Joab’s revenge     A. Bitterness\n"
                     "2. David’s mourning   B. Honour\n"
                     "3. Abner’s promise    C. Diplomacy\n")
    return questions

def generate_meditative_questions(verses):
    questions = []
    linked_verses = [
        "Romans 12:19",
        "Philippians 4:6",
        "John 14:27",
        "Isaiah 41:10"
    ]
    for _ in range(4):
        verse = random.choice(verses)
        summary = verse[:80] + ("..." if len(verse) > 80 else "")
        linked_verse = random.choice(linked_verses)
        q = random.choice(MEDITATIVE_TEMPLATES).format(
            verse_summary=summary, linked_verse=linked_verse
        )
        questions.append("🧬🦠 " + q)
    return questions

def display_chapter_quiz(book, chapter, verses):
    print(f"\n📖 TODAY'S HOPE MEDITATIVE BIBLE QUIZ FROM {book} {chapter}:")
    for i, v in enumerate(verses[:5], 1):
        print(f"{i}. {v}")

    print("\n🧪 QUIZ QUESTIONS:")
    for q in generate_direct_questions(verses):
        print(q)
    for q in generate_meditative_questions(verses):
        print(q)

def main():
    if len(sys.argv) != 4:
        print("Usage: python meditative_quiz.py <BookName> <ChapterNumber> <BibleFile>")
        return

    book = sys.argv[1]
    chapter = sys.argv[2]
    file_path = sys.argv[3]

    print(f"[INFO] Loading {book} chapter {chapter} from {file_path}...")
    bible_data = load_bible(file_path)
    verses = get_chapter_verses(bible_data, book, chapter)

    if verses:
        display_chapter_quiz(book, chapter, verses)
    else:
        print("No verses found.")

if __name__ == "__main__":
    main()
