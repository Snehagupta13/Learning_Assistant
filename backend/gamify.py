from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import os
import torch
# Initialize Groq LLM
from dotenv import load_dotenv
import streamlit as st
# Initialize Groq LLM
# 1. Load variables from .env file first
load_dotenv()

# 2. Access keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

if not GROQ_API_KEY:
    st.error("⚠️ GROQ_API_KEY is missing. Please set it in your .env file.")
else:
    # 3. Initialize Groq LLM only after key is loaded
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=GROQ_API_KEY
    )

from langchain.prompts import ChatPromptTemplate


def gamify_doc(topic, length="medium", context=""):
    """
    Generate an interactive single-file HTML/CSS/JS learning document
    for the given topic.
    """

    prompt = ChatPromptTemplate.from_template("""
You are an expert educational content generator.

Create a **complete intrative ,gamified website using html,css ,javascript in a single file** about the topic: "{topic}".

Rules:
- Must start with <!DOCTYPE html> and include <html>, <head>, and <body>.
- Inline CSS must be inside a <style> tag in <head>.
- Inline JavaScript must be inside a <script> tag.
- ⚠️ Absolutely do NOT use Markdown formatting (no **bold**, no ## headings, no ``` fences).
- Only output raw HTML. Nothing else.

Length: {length}
Context: {context}
""")
 


    chain = prompt | llm
    response = chain.invoke({
        "topic": topic,
        "length": length,
        "context": context
    })

    return response.content.strip()

