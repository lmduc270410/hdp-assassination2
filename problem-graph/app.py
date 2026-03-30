import streamlit as st
import json
import requests
import numpy as np
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pyvis.network import Network
import tempfile
import os

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
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive"
    }

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    return soup.get_text()[:8000]

# =========================
# OLLAMA
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

def extract_json(text):
    try:
        return json.loads(text)
    except:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end+1])
            except:
                pass
    return None

def generate_problem(text):
    prompt = f"""
Extract JSON:

{{
"id": "...",
"title": "...",
"tags": [],
"techniques": [],
"algorithmic_signature": "...",
"embedding_text": "..."
}}

ONLY JSON.

TEXT:
{text}
"""
    raw = call_ollama(prompt)
    return extract_json(raw)

# =========================
# GRAPH
# =========================
def build_graph(problem_data):
    if len(problem_data) < 2:
        return None

    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [p.get("embedding_text", "") for p in problem_data]
    emb = model.encode(texts)

    sim = cosine_similarity(emb)

    net = Network(height="600px", width="100%")

    for i, p in enumerate(problem_data):
        net.add_node(i, label=p["id"], title=p.get("algorithmic_signature", ""))

    for i in range(len(problem_data)):
        for j in range(i+1, len(problem_data)):
            if sim[i][j] > 0.5:
                net.add_edge(i, j, value=sim[i][j])

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.write_html(tmp.name)
    return tmp.name

# =========================
# UI
# =========================
st.title("🧠 Problem Graph AI")

db = load_db()

# ---- ADD PROBLEM ----
st.header("➕ Add Problem")
link = st.text_input("Paste problem link")

if st.button("Add"):
    if link:
        text = fetch_text(link)
        item = generate_problem(text)

        if item:
            item["link"] = link
            db.append(item)
            save_db(db)
            st.success(f"Added {item['id']}")
        else:
            st.error("Failed to parse")

# ---- SEARCH ----
st.header("🔍 Search")
query = st.text_input("Search idea (e.g. binary search dp)")

if query and db:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    q_emb = model.encode([query])

    texts = [p.get("embedding_text", "") for p in db]
    emb = model.encode(texts)

    sims = cosine_similarity(q_emb, emb)[0]
    top = np.argsort(sims)[-5:][::-1]

    for i in top:
        st.write(f"{db[i]['id']} - {db[i].get('algorithmic_signature','')}")

# ---- GRAPH ----
st.header("🌐 Graph")

if st.button("Build Graph"):
    path = build_graph(db)
    if path:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        st.components.v1.html(html, height=600)