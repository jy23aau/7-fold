import json
import random
import sys

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

    # Fill in the blank (x2)
    for _ in range(2):
        verse = random.choice(verses)
        words = verse.split()
        if len(words) > 5:
            blank = random.choice(words)
            blanked = verse.replace(blank, "____", 1)
            questions.append(f"🦠 Fill in the blank: {blanked}")
        else:
            questions.append(f"🦠 True or False: {verse}")

    # Match-the-following (fixed sample)
    questions.append(
        "🧬🦠 Match the Following – Match the character or action with the spiritual theme:\n\n"
        "A (Person/Act)        B (Spiritual Theme)\n"
        "1. Joab’s revenge     A. Bitterness\n"
        "2. David’s mourning   B. Honour\n"
        "3. Abner’s promise    C. Diplomacy\n"
    )

    return questions

def generate_meditative_questions(verses):
    linked_verses = [
        "Romans 12:19", "Philippians 4:6", "John 14:27", "Isaiah 41:10",
        "Matthew 5:44", "Psalm 23:1", "Galatians 5:22"
    ]

    questions = []
    for _ in range(4):
        verse = random.choice(verses)
        summary = verse[:90] + ("..." if len(verse) > 90 else "")
        link = random.choice(linked_verses)
        q = random.choice(MEDITATIVE_TEMPLATES).format(
            verse_summary=summary, linked_verse=link
        )
        questions.append("🧬🦠 " + q)
    return questions

def display_chapter_quiz(book, chapter, verses):
    print(f"\n📖 *TODAY'S HOPE MEDITATIVE BIBLE QUIZ FROM {book} {chapter}*")
    print("-" * 60)
    for i, v in enumerate(verses[:5], 1):
        print(f"{i}. {v}")
    print("-" * 60)

    print("\n🧪 *7 Spiritual Questions*:\n")

    all_questions = generate_direct_questions(verses) + generate_meditative_questions(verses)
    for idx, q in enumerate(all_questions, 1):
        print(f"{idx}. {q}\n")

def main():
    if len(sys.argv) != 4:
        print("Usage: python bible_meditative_agent.py <BookName> <ChapterNumber> <BibleFile>")
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
