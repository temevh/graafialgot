import networkx as nx
from networkx.algorithms.community import girvan_newman

G = nx.Graph()
G.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (6, 7)])

communities = girvan_newman(G)

next(communities)
next(communities)

for i, community in enumerate(next(communities), 1):
    print(f"Community {i}: {list(community)}")