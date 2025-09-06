import json, os
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px

PROGRESS_FILE = "data/progress.json"

# ---------- Data Handling ----------
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return []

def save_progress(progress):
    os.makedirs("data", exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def log_attempt(topic, difficulty, score, total):
    progress = load_progress()
    attempt = {
        "topic": topic,
        "difficulty": difficulty,
        "score": score,
        "total": total,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    progress.append(attempt)
    save_progress(progress)

def get_badges(progress):
    badges = []
    if len(progress) >= 1:
        badges.append("🥇 First Quiz Completed")
    if any(p["score"] == p["total"] for p in progress):
        badges.append("✅ Perfect Score")
    if len({p["topic"] for p in progress}) >= 3:
        badges.append("🎓 3 Topics Attempted")
    return badges


