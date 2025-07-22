import streamlit as st
import json
import random
import os

# --- Custom CSS Styling with Blue Background & Yellow Header & Image Overlay ---
st.markdown("""
    <style>
    body, .stApp {
        background-color: #001f3f !important;
        color: #fff !important;
        background-image: url('bg_overlay.png');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        opacity: 0.96;
    }
    .light-yellow-heading, h1, h2, h3 {
        color: #FFF59D !important;
        font-weight: bold !important;
        font-family: 'Arial Black', Arial, sans-serif !important;
    }
    .bold-tool-title {
        color: #FFD700 !important;
        font-size: 2.2em !important;
        font-weight: bold !important;
        letter-spacing: 0.01em;
        margin: 0.8em 0 1.8em 0 !important;
        padding-bottom: 0.2em;
        font-family: 'Arial Black', Arial, sans-serif !important;
        display: block;
        text-align: center;
    }
    .white-font {
        color: #fff !important;
        font-family: 'Arial', sans-serif !important;
    }
    .stRadio label, .st-selectbox label, .stExpanderHeader {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.1em !important;
    }
    div[role='radiogroup'] {
        background: rgba(30,30,30,0.25) !important;
        padding: 14px 10px 7px 10px !important;
        border-radius: 12px !important;
        margin-bottom: 1.3em;
        margin-top: 0.5em;
        box-shadow: 0 2px 12px #FFD70033;
    }
    div[role='radiogroup'] label {
        font-size: 1.1em !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        border-radius: 7px !important;
        background: #1c1c1c !important;
        padding: 7px 18px !important;
        margin: 7px 10px !important;
        transition: background 0.22s, color 0.22s;
        box-shadow: 0 0 6px #FFD70044;
    }
    div[role='radiogroup'] label:hover, div[role='radiogroup'] label:focus {
        background: #FFF9C422 !important;
        color: #000 !important;
    }
    table.match-following-table {
        width: 80%% !important;
        margin: 0.7em 0 1.1em 0 !important;
        font-size: 1.1em;
        border-collapse: separate;
        border-spacing: 0 6px;
    }
    table.match-following-table td {
        border: none !important;
        padding: 0.35em 1.3em 0.35em 0.3em !important;
        color: #fff !important;
        background: #222 !important;
        border-radius: 8px;
        vertical-align: middle;
        font-family: 'Arial', sans-serif !important;
    }
    table.match-following-table th {
        color: #FFD700 !important;
        background: transparent !important;
        font-size: 1.13em !important;
        text-align: left;
        padding-bottom: 0.28em;
        border: none !important;
        font-weight: 900;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_bible(version_file):
    with open(version_file, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def get_chapter_count(bible_data, book):
    for b in bible_data:
        if b['name'].lower() == book.lower():
            return len(b['chapters'])
    return 0

def get_chapter_verses(bible_data, book, chapter):
    try:
        book_data = next(b for b in bible_data if b['name'].lower() == book.lower())
        return book_data['chapters'][int(chapter) - 1]
    except Exception:
        return []

def light_yellow_heading(text, level=2):
    return f"<h{level} class='light-yellow-heading' style='margin-top:1.2em;margin-bottom:0.8em;'>{text}</h{level}>"

def generate_direct_questions(verses, reference):
    questions = []
    filled = 0
    randomized = verses.copy()
    random.shuffle(randomized)
    for verse in randomized:
        words = verse.split()
        if len(words) > 5 and filled < 2:
            blank = random.choice(words)
            blanked = verse.replace(blank, "____", 1)
            questions.append({
                "heading": "Fill in the blank",
                "text": blanked,
                "reference": f"({reference})"
            })
            filled += 1
        if filled == 2: break
    for verse in randomized:
        if len(questions) >= 2: break
        questions.append({
            "heading": "True or False",
            "text": verse,
            "reference": f"({reference})"
        })
    questions.append({
        "heading": "Match the Following",
        "is_table": True,
        "reference": "",
        "table_data": [
            ["Joab’s revenge", "A. Bitterness"],
            ["David’s mourning", "B. Honour"],
            ["Abner’s promise", "C. Diplomacy"],
        ]
    })
    return questions

def generate_meditative_questions(verses, reference):
    templates = [
        ("Reflect", "Reflect on this: What does {summary} reveal about God's character?"),
        ("Think Deeper", "Think deeper: How can {summary} guide your spiritual walk today?"),
        ("Lesson", "What lesson does {summary} hold that aligns with {reference}?"),
        ("Compare", "Compare {summary} with {reference}: What truth stands out?"),
    ]
    refs = [
        "Romans 12:19", "Philippians 4:6", "John 14:27",
        "Isaiah 41:10", "Matthew 5:44", "Psalm 23:1", "Galatians 5:22"
    ]
    questions = []
    for heading, template in templates:
        verse = random.choice(verses)
        summary = verse[:80] + ("..." if len(verse) > 80 else "")
        ref = random.choice(refs)
        text = template.format(summary=summary, reference=ref)
        questions.append({
            "heading": heading,
            "text": text,
            "reference": f"({ref})"
        })
    return questions

# --- PAGE RENDERING ---

st.markdown("<div class='bold-tool-title'>Bible Meditative Tool</div>", unsafe_allow_html=True)

bible_versions = [f for f in os.listdir() if f.endswith('.json')]
version = st.selectbox("**Select Bible Version:**", bible_versions)
bible_data = load_bible(version)

old_testament_books = [ ... ]  # (same as before, or load from file)
old_testament = [b['name'] for b in bible_data if b['name'] in old_testament_books]
new_testament = [b['name'] for b in bible_data if b['name'] not in old_testament_books]

selected_testament = st.radio("**Choose Testament:**", ["Old Testament", "New Testament"])
filtered_books = old_testament if selected_testament == "Old Testament" else new_testament
book = st.selectbox("**Select Book:**", filtered_books)
chapter_count = get_chapter_count(bible_data, book)
chapter = st.selectbox("**Select Chapter:**", [str(c) for c in range(1, chapter_count+1)])

with st.expander("📘 Introduction & Background Study", expanded=True):
    st.markdown(f"<span class='white-font'><b>This is a brief background of {book} {chapter}.</b></span>", unsafe_allow_html=True)

verses = get_chapter_verses(bible_data, book, chapter)

with st.expander("📖 Read This Chapter"):
    for i, v in enumerate(verses, 1):
        st.markdown(f"<span class='white-font'><b>{i}.</b> {v}</span>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

if st.button("Generate Quiz"):
    st.markdown(light_yellow_heading("Quiz Questions", 2), unsafe_allow_html=True)
    st.markdown("<div style='color:#fff;font-size:1.13em;font-weight:bold;margin-bottom:1.2em;'>Today's Hope Meditative Bible Quiz</div>", unsafe_allow_html=True)
    if verses:
        ref = f"{book} {chapter}"
        all_questions = generate_direct_questions(verses, ref) + generate_meditative_questions(verses, ref)
        for idx, q in enumerate(all_questions, 1):
            if q.get("is_table"):
                st.markdown(f"""<div style='margin-bottom:1.5em;'>
                <span class='white-font'><b>{idx}.</b></span><br>
                <span class='light-yellow-heading' style='font-size:1.08em;margin-bottom:2px'>{q['heading']}</span>
                <table class="match-following-table">
                    <tr><th>A (Person/Act)</th><th>B (Spiritual Theme)</th></tr>
                    <tr><td>Joab’s revenge</td><td>A. Bitterness</td></tr>
                    <tr><td>David’s mourning</td><td>B. Honour</td></tr>
                    <tr><td>Abner’s promise</td><td>C. Diplomacy</td></tr>
                </table></div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style='margin-bottom:1.6em;'>
                <span class='white-font'><b>{idx}.</b></span><br>
                <span class='light-yellow-heading' style='font-size:1.08em;margin-bottom:2px'>{q['heading']}</span><br>
                <span class='white-font'>{q['text']} <i>{q['reference']}</i></span>
                </div>""", unsafe_allow_html=True)
    else:
        st.warning("No verses found for that book/chapter.")
