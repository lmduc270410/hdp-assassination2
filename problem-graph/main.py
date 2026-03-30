import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from pyvis.network import Network

# =========================
# LOAD DATA
# =========================

with open("data/problems.json", "r", encoding="utf-8") as f:
    problem_data = json.load(f)

# =========================
# BUILD FEATURES
# =========================

all_tags = sorted({t for p in problem_data for t in p.get("tags", [])})
all_techniques = sorted({t for p in problem_data for t in p.get("techniques", [])})

def build_vector(p):
    tag_vec = [1 if t in p.get("tags", []) else 0 for t in all_tags]
    tech_vec = [1 if t in p.get("techniques", []) else 0 for t in all_techniques]
    return np.array(tag_vec + tech_vec, dtype=float)

symbolic_vectors = np.array([build_vector(p) for p in problem_data])

# =========================
# EMBEDDING
# =========================

model = SentenceTransformer("all-MiniLM-L6-v2")
texts = [p.get("embedding_text", "") for p in problem_data]
embeddings = model.encode(texts)

# =========================
# COMBINE
# =========================

final_vectors = np.concatenate([
    symbolic_vectors * 1.0,
    embeddings * 2.0
], axis=1)

sim_matrix = cosine_similarity(final_vectors)

# =========================
# BUILD GRAPH
# =========================

k = 3
edges = set()

for i in range(len(problem_data)):
    sims = sim_matrix[i]
    neighbors = np.argsort(sims)[-k-1:-1]

    for j in neighbors:
        if i != j:
            a, b = sorted((int(i), int(j)))
            edges.add((a, b, float(sims[j])))

# =========================
# VISUALIZE
# =========================

net = Network(height="800px", width="100%")

for i, p in enumerate(problem_data):
    net.add_node(
        int(i),
        label=p["id"],
        title=p.get("algorithmic_signature", ""),
        size=25
    )

for i, j, w in edges:
    net.add_edge(int(i), int(j), width=2 + w * 5)

net.barnes_hut()
net.write_html("graph.html")

print("✅ Open graph.html")