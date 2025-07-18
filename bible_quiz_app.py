import streamlit as st
import json
import random
import os

# --- Load Bible JSON ---
@st.cache_data
def load_bible(version_file):
    with open(version_file, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

# --- Get all book names from the Bible data ---
def get_book_names(bible_data):
    return [book['name'] for book in bible_data]

# --- Get chapter count for a selected book ---
def get_chapter_count(bible_data, book):
    for b in bible_data:
        if b['name'].lower() == book.lower():
            return len(b['chapters'])
    return 0

# --- Get Verses from Book and Chapter ---
def get_chapter_verses(bible_data, book, chapter):
    try:
        book_data = next(b for b in bible_data if b['name'].lower() == book.lower())
        return book_data['chapters'][int(chapter) - 1]
    except Exception as e:
        st.error(f"Error fetching chapter: {e}")
        return []

# --- Generate Questions ---
def generate_direct_questions(verses):
    questions = []
    for _ in range(3):
        verse = random.choice(verses)
        words = verse.split()
        if len(words) > 5:
            blanked = verse.replace(random.choice(words), "____", 1)
            questions.append(f"🦠 Fill in the blank: {blanked}")
        else:
            questions.append(f"🦠 True or False: {verse}")
    return questions

def generate_meditative_questions(verses):
    questions = []
    for _ in range(4):
        verse = random.choice(verses)
        summary = verse[:80] + ("..." if len(verse) > 80 else "")
        linked_verse = "Romans 12:19"
        q = random.choice([
            f"Reflect on this: What does {summary} reveal about God's character?",
            f"Think deeper: How can {summary} guide your spiritual walk today?",
            f"What lesson does {summary} hold that aligns with {linked_verse}?",
            f"Compare {summary} with {linked_verse}: What truth stands out?"
        ])
        questions.append("🧬🦠 " + q)
    return questions

# --- Streamlit UI ---
st.title("📖 Today's Hope - Meditative Bible Quiz")

# Find all .json files in the current directory for Bible versions
bible_versions = [f for f in os.listdir() if f.endswith('.json')]
version = st.selectbox("Select Bible Version:", bible_versions)

# Load Bible data
bible_data = load_bible(version)

# Testament Filter
old_testament_books = [b['name'] for b in bible_data if b['name'] in [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua",
    "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
    "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job",
    "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah",
    "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai",
    "Zechariah", "Malachi"]]

new_testament_books = [b['name'] for b in bible_data if b['name'] not in old_testament_books]

selected_testament = st.radio("Choose Testament:", ["Old Testament", "New Testament"])

if selected_testament == "Old Testament":
    filtered_books = old_testament_books
else:
    filtered_books = new_testament_books

# Book and Chapter Dropdowns
book = st.selectbox("Select Book:", filtered_books)
chapter_count = get_chapter_count(bible_data, book)
chapter = st.selectbox("Select Chapter:", list(map(str, range(1, chapter_count + 1))))

# Show background and full chapter sections
with st.expander("📘 Introduction & Background Study"):
    st.write(f"This is a brief background of {book} {chapter}. Who wrote it, the purpose, and key message.")

with st.expander("📖 Read This Chapter"):
    verses = get_chapter_verses(bible_data, book, chapter)
    for i, v in enumerate(verses, 1):
        st.markdown(f"{i}. {v}")

# Quiz Generator Button
if st.button("Generate Quiz"):
    if verses:
        st.markdown("## 🧪 Quiz Questions")
        for q in generate_direct_questions(verses):
            st.markdown(q)
        for q in generate_meditative_questions(verses):
            st.markdown(q)
    else:
        st.warning("No verses found for that book/chapter.")
