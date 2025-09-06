import wikipedia

def fetch_context(topic):
    """Fetch short Wikipedia context for RAG"""
    try:
        summary = wikipedia.summary(topic, sentences=5)
        return summary
    except Exception:
        return "No additional context found."
import wikipedia
from bs4 import BeautifulSoup

# Patch wikipedia to always use lxml
def patched_beautifulsoup(*args, **kwargs):
    kwargs["features"] = "lxml"
    return original_bs(*args, **kwargs)

original_bs = BeautifulSoup
wikipedia.BeautifulSoup = patched_beautifulsoup
