import streamlit as st
import textstat
import random
import time

# Page setup
st.set_page_config(page_title="DetectAI - AI Content Detector", layout="centered")
st.title("🧠 DetectAI: Is This Text Human or AI-Generated?")

# Instructions
st.markdown("""
Paste any text below, and our tool will analyze whether it's likely written by a human or AI.
The analysis uses readability scores, sentence length, and content length.
""")

# Text input
user_input = st.text_area("📋 Enter your text here:", height=250)

# Detection logic
def detect_ai(text):
    if len(text.strip()) == 0:
        return None, None, []

    readability = textstat.flesch_reading_ease(text)
    sentences = text.split('.')
    avg_length = sum(len(s.split()) for s in sentences if s) / max(len(sentences), 1)

    score = 0
    explanation = []

    if readability > 60:
        score += 30
        explanation.append("High readability – often found in AI-generated text.")
    else:
        explanation.append("Moderate readability – more typical of human writing.")

    if avg_length < 20:
        score += 40
        explanation.append("Short, consistent sentence length – common in AI writing.")
    else:
        explanation.append("Varied sentence length – typical of human writing.")

    if len(text.split()) > 100:
        score += 20
        explanation.append("Long-form content detected – can be either human or AI.")
    else:
        explanation.append("Short content.")

    # Add randomness (optional for simulation)
    score += random.randint(-10, 10)
    score = max(0, min(100, score))

    label = "🧠 Likely AI-Generated" if score > 60 else "🧍 Likely Human-Written"
    return score, label, explanation

# Button logic
if st.button("🔍 Analyze Text"):
    with st.spinner("Analyzing..."):
        time.sleep(1.5)
        score, label, explanation = detect_ai(user_input)

    if score is not None:
        st.success(f"**Confidence Score:** {score}%")
        st.markdown(f"### Result: {label}")
        with st.expander("🔎 Why this result?"):
            for reason in explanation:
                st.markdown(f"- {reason}")
    else:
        st.warning("Please enter some text.")
