import json
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import re
import os
import streamlit as st

from dotenv import load_dotenv
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


def generate_quiz(topic, difficulty="medium"):
    prompt = ChatPromptTemplate.from_template("""
    You are a quiz generator.

    Create a {difficulty}-level quiz on the topic "{topic}".

    Requirements:
    - 5 questions total
    - Mix: 4 multiple-choice (MCQ, 4 options each) + 1 fill-in-the-blank
    - Provide correct answers
    - Respond ONLY in JSON, no explanations.

    Format:
    {{
      "questions": [
        {{
          "type": "mcq",
          "question": "What is an array?",
          "options": ["A data type", "A data structure", "A function", "A loop"],
          "answer": "A data structure"
        }},
        {{
          "type": "fill",
          "question": "An array stores elements of ____ type.",
          "answer": "same"
        }}
      ]
    }}
    """)

    chain = prompt | llm
    raw = chain.invoke({"topic": topic, "difficulty": difficulty}).content.strip()

    # Strip code fences if present
    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z]*\n", "", raw)
        raw = raw.rstrip("```").strip()

    try:
        data = json.loads(raw)
        quiz = data.get("questions", [])
        answers = {i+1: q["answer"] for i, q in enumerate(quiz)}
        return quiz, answers
    except Exception as e:
        st.error("⚠️ Failed to parse quiz JSON.")
        st.code(raw)   # Show raw output in UI for debugging
        return [], {}


def evaluate_quiz(user_answers, correct_answers):
    """Compare user answers with correct answers"""
    score = 0
    feedback = ""
    for idx, ans in user_answers.items():
        correct = correct_answers.get(idx, "")
        if ans.strip().lower() == correct.strip().lower():
            score += 1
            feedback += f"✅ Q{idx}: Correct!\n"
        else:
            feedback += f"❌ Q{idx}: Your answer: {ans}, Correct: {correct}\n"
    return f"{score}/{len(correct_answers)}", feedback
