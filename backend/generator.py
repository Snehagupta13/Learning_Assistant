from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import os
import torch
import streamlit as st
from dotenv import load_dotenv
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
        model="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY
    )



from langchain.prompts import ChatPromptTemplate

def generate_doc(topic, doc_type="pre", length="medium", context=""):
    """
    Generate Pre/Post class document.
    Returns text content (string).
    """

    if doc_type == "pre":
        prompt = ChatPromptTemplate.from_template("""
        You are an interactive learning assistant.
        Generate a **Pre-Class Learning Document** on the topic: {topic}.
        
        Guidelines:
        - Document length: {length}
        - Cover prerequisites, foundational concepts, learning goals, and key terminologies.
        - Use this context if relevant: {context}
        - Present in a professional, student-friendly style.
        - Use structured headings, bullet points, tables, and clear formatting.
        - Add relevant diagrams/images (if helpful) in this format:
          "Image: diagram of array indexing"
          "Image: visualization of stack push and pop"
        - Ensure it prepares students for the class.
        """)

    else:  # post-class
        prompt = ChatPromptTemplate.from_template("""
        You are an interactive learning assistant.
        Generate a **Post-Class Learning Document** on the topic: {topic}.
        
        Guidelines:
        - Document length: {length}
        - Provide a concise summary of the topic.
        - Highlight key takeaways, real-world examples, and revision notes.
        - Use structured headings, bullet points, tables, and clear formatting.
        - Add optional mind-maps/diagrams for easy retention (if applicable) in this format:
          "Image: mind map of key concepts"
          "Image: flowchart of process"
        - Make it suitable for revision after class.
        - Ensure the tone is professional and student-friendly.
        """)

    chain = prompt | llm
    response = chain.invoke({
        "topic": topic,
        "doc_type": doc_type,
        "length": length,
        "context": context
    })

    return response.content.strip()


   


