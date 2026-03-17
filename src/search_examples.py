# search_examples.py
from serpapi import GoogleSearch
from config import SERP_API_KEY

def search_examples(word):
    params = {
        "engine": "google",
        "q": f'"{word}" example sentence',
        "api_key": SERP_API_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    examples = [r.get("snippet") for r in results.get("organic_results", []) if r.get("snippet")]
    return examples[:5]