import matplotlib.pyplot as plt
import networkx as nx
import json

from graph.build_graph import build_graph

print("RUNNING...")

# -------------------------------
# LOAD DATA
# -------------------------------
with open("data/synthetic_dataset.json", "r") as f:
    dataset = json.load(f)

G = build_graph(dataset)

print("Nodes:", len(G.nodes()))
print("Edges:", len(G.edges()))

plt.figure(figsize=(14, 10))

# -------------------------------
# HIERARCHICAL POSITIONING
# -------------------------------
pos = {}

companies = [n for n, d in G.nodes(data=True) if d["type"] == "company"]
teams = [n for n, d in G.nodes(data=True) if d["type"] == "team"]
users = [n for n, d in G.nodes(data=True) if d["type"] == "user"]

# --- Companies ---
for i, company in enumerate(companies):
    pos[company] = (i * 6, 2)

# --- Teams under companies ---
team_positions = {}

for company in companies:
    company_teams = [t for t in teams if G.nodes[t]["company_id"] == company]
    base_x = pos[company][0]

    for j, team in enumerate(company_teams):
        x = base_x + (j - 1) * 2
        pos[team] = (x, 1)
        team_positions[team] = x

# --- Users under teams ---
for team in teams:
    team_users = [u for u in users if G.nodes[u]["team_id"] == team]
    base_x = team_positions[team]

    for k, user in enumerate(team_users):
        x = base_x + (k - 1) * 0.6
        pos[user] = (x, 0)

# -------------------------------
# COLORS
# -------------------------------
color_map = []
for node in G.nodes(data=True):
    if node[1]["type"] == "user":
        color_map.append("skyblue")
    elif node[1]["type"] == "team":
        color_map.append("lightgreen")
    else:
        color_map.append("orange")

# -------------------------------
# ONLY HIERARCHY EDGES
# -------------------------------
hierarchy_edges = [
    (u, v) for u, v, d in G.edges(data=True)
    if d.get("edge_type") == "belongs_to"
]

# -------------------------------
# DRAW GRAPH
# -------------------------------
nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=800)

nx.draw_networkx_edges(
    G, pos,
    edgelist=hierarchy_edges,
    edge_color="black",
    width=2
)

nx.draw_networkx_labels(G, pos, font_size=8)

# -------------------------------
# LEGEND
# -------------------------------
import matplotlib.patches as mpatches

user_patch = mpatches.Patch(color='skyblue', label='User')
team_patch = mpatches.Patch(color='lightgreen', label='Team')
company_patch = mpatches.Patch(color='orange', label='Company')

plt.legend(handles=[user_patch, team_patch, company_patch])

# -------------------------------
# FINAL DISPLAY
# -------------------------------
plt.title("WorkTrust Graph (Clean Hierarchy)")
plt.axis("off")

print("SHOWING GRAPH...")
plt.show()