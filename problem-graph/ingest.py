import json
import requests
from bs4 import BeautifulSoup

DATA_PATH = "data/problems.json"

# =========================
# LOAD / SAVE
# =========================

def load_db():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_db(db):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

# =========================
# FETCH TEXT
# =========================

def fetch_text(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text()
    return text[:8000]  # limit size

# =========================
# OLLAMA CALL
# =========================

def call_ollama(prompt):
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return res.json()["response"]

# =========================
# PARSE JSON SAFELY
# =========================

def extract_json(text):
    try:
        return json.loads(text)
    except:
        # try to extract JSON block
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end+1])
            except:
                pass
    return None

# =========================
# GENERATE PROBLEM
# =========================

def generate_problem(text):
    prompt = f"""
You are an expert competitive programmer.

Extract structured data in STRICT JSON:

{{
"id": "short id like P1314",
"title": "...",
"tags": ["dp", "greedy", "binary_search", "graph"],
"techniques": ["kadane", "difference_array", "binary_search_on_answer"],
"data_structures": ["array", "segment_tree", "priority_queue"],
"algorithmic_signature": "short description of solution idea",
"embedding_text": "1 sentence describing core idea"
}}

ONLY RETURN JSON. NO EXPLANATION.

TEXT:
{text}
"""

    for _ in range(3):  # retry
        raw = call_ollama(prompt)
        data = extract_json(raw)
        if data:
            return data

    print("❌ Failed to parse JSON")
    print(raw)
    return None

# =========================
# MAIN
# =========================
def main():
    with open("links.txt") as f:
        links = [line.strip() for line in f if line.strip()]

    db = load_db()

    for link in links:
        print(f"\n🔗 {link}")

        text = fetch_text(link)
        item = generate_problem(text)

        if item:
            item["link"] = link
            db.append(item)
            print("✅", item["id"])

    save_db(db)

if __name__ == "__main__":
    main()