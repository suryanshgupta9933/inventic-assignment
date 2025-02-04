# Importingf Dependencies
import streamlit as st

from src.pipeline import summarize_text, detect_emotion, search_book, count_words

def app():
    st.set_page_config(page_title="Assignment", page_icon="📚", layout="centered")
    st.title("Assignment")
    st.markdown("This app analyzes the book passage and provides insights on the same.")

    st.markdown("Please upload the book passage in the text box below.")
    text = st.text_area("Enter Text")

    if st.button("Analyze"):
        with st.spinner("Analyzing the text..."):
            summary = summarize_text(text)
            st.markdown("### Summary")
            st.write(summary)
            emotion = detect_emotion(text)
            st.markdown("### Emotion")
            st.write(emotion)
            book = search_book(text)
            st.markdown("### Book")
            st.write(book)
            word_count = count_words(text)
            st.markdown("### Word Count")
            st.write(word_count)

if __name__ == "__main__":
    app()