import streamlit as st
import re

st.title("WhatsApp Chat Analyzer")

uploaded_file = st.file_uploader("Upload WhatsApp Chat (.txt)")

if uploaded_file is not None:
    data = uploaded_file.read().decode("utf-8")

    st.write("Preview of Chat")
    st.text(data[:500])

    pattern = r'\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'
    messages = re.split(pattern, data)[1:]

    st.write("Total Messages:", len(messages))