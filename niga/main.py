import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from pyvis.network import Network

# =========================
# DATA
# =========================

problem_data = [
    {
        "id": "P1314",
        "title": "聪明的质监员",
        "tags": ["binary_search", "prefix_sum"],
        "techniques": ["binary_search_on_answer", "range_sum_query", "prefix_sum_optimization"],
        "algorithmic_signature": "binary search on answer + prefix sum check",
        "embedding_text": "Optimize a threshold value using binary search with prefix sums."
    },
    {
        "id": "P8218",
        "title": "Queue Problem",
        "tags": ["greedy", "data_structures"],
        "techniques": ["greedy_selection", "sorting", "simulation"],
        "algorithmic_signature": "sorting + greedy with priority queue",
        "embedding_text": "Construct ordering using greedy and priority queue."
    },
    {
        "id": "P1719",
        "title": "最大加权矩形",
        "tags": ["dp", "prefix_sum"],
        "techniques": ["2d_to_1d_reduction", "kadane_algorithm"],
        "algorithmic_signature": "fix rows + Kadane",
        "embedding_text": "Reduce 2D matrix to 1D and apply Kadane."
    },
    {
        "id": "P2882",
        "title": "Face The Right Way",
        "tags": ["greedy", "prefix_sum"],
        "techniques": ["difference_array", "greedy_flipping"],
        "algorithmic_signature": "greedy + difference array",
        "embedding_text": "Greedy flipping with difference array."
    },
    {
        "id": "P4552",
        "title": "IncDec Sequence",
        "tags": ["greedy", "math"],
        "techniques": ["difference_array", "greedy_adjustment"],
        "algorithmic_signature": "difference array balancing",
        "embedding_text": "Balance positive and negative differences."
    }
]

# =========================
# BUILD FEATURES
# =========================

all_tags = sorted({t for p in problem_data for t in p["tags"]})
all_techniques = sorted({t for p in problem_data for t in p["techniques"]})

def build_vector(p):
    tag_vec = [1 if t in p["tags"] else 0 for t in all_tags]
    tech_vec = [1 if t in p["techniques"] else 0 for t in all_techniques]
    return np.array(tag_vec + tech_vec)

symbolic_vectors = np.array([build_vector(p) for p in problem_data])

# =========================
# EMBEDDING
# =========================

model = SentenceTransformer('all-MiniLM-L6-v2')
texts = [p["embedding_text"] for p in problem_data]
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
# BUILD GRAPH (FIXED)
# =========================

k = 3

edges = set()  # remove duplicates

for i in range(len(problem_data)):
    sims = sim_matrix[i]
    neighbors = np.argsort(sims)[-k-1:-1]

    for j in neighbors:
        if i != j:
            a, b = min(i, j), max(i, j)
            edges.add((int(a), int(b), float(sims[j])))

# =========================
# VISUALIZATION (IMPROVED)
# =========================

net = Network(height="700px", width="100%")

# Color by main tag
def get_color(p):
    if "dp" in p["tags"]:
        return "red"
    if "greedy" in p["tags"]:
        return "green"
    if "binary_search" in p["tags"]:
        return "blue"
    return "gray"

# Nodes
for i, p in enumerate(problem_data):
    net.add_node(
        int(i),
        label=p["id"],
        title=f"{p['title']}<br>{p['algorithmic_signature']}",
        color=get_color(p),
        size=25
    )

# Normalize weights for visibility
weights = [w for (_, _, w) in edges]
min_w, max_w = min(weights), max(weights)

def scale(w):
    if max_w == min_w:
        return 5
    return 2 + 8 * (w - min_w) / (max_w - min_w)

# Edges
for i, j, w in edges:
    net.add_edge(
        int(i), int(j),
        value=float(w),
        width=scale(w),   # 🔥 key fix
        title=f"sim={round(w,3)}"
    )

# Better physics
net.barnes_hut()
net.show_buttons(filter_=['physics'])

net.write_html("graph.html")

print("Graph generated: open graph.html")

# =========================
# SEARCH FUNCTION
# =========================

def find_similar(problem_id, top_k=3):
    idx = next(i for i, p in enumerate(problem_data) if p["id"] == problem_id)
    sims = sim_matrix[idx]
    order = np.argsort(-sims)

    print(f"\nSimilar to {problem_id}:")
    for i in order[1:top_k+1]:
        print(problem_data[i]["id"], "score:", round(sims[i], 3))


find_similar("P2882")