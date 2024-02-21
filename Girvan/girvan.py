def edge_betweenness(graph):
    betweenness = {edge: 0 for edge in graph['edges']}
    betweenness.update({(v, u): 0 for (u, v) in betweenness.keys()})
    for node in graph['nodes']:
        stack, paths, dist = [], {v: [] for v in graph['nodes']}, {v: float('inf') for v in graph['nodes']}
        stack.append(node)
        paths[node] = [[node]]
        dist[node] = 0
        while stack:
            v = stack.pop(0)
            for w in graph[v]:
                if dist[w] == float('inf'):
                    stack.append(w)
                    dist[w] = dist[v] + 1
                if dist[w] == dist[v] + 1:
                    paths[w].extend([path + [w] for path in paths[v]])
        node_betweenness = {edge: 0 for edge in betweenness.keys()}
        for path in [path for paths in paths.values() for path in paths]:
            for edge in zip(path[:-1], path[1:]):
                node_betweenness[edge] += 1
        for edge in betweenness.keys():
            betweenness[edge] += node_betweenness[edge] / 2
    return betweenness

def remove_edge(graph, edge):
    graph[edge[0]].remove(edge[1])
    graph[edge[1]].remove(edge[0])
    graph['edges'].remove(edge)

def connected_components(graph):
    visited = {node: False for node in graph['nodes']}
    def dfs(v):
        visited[v] = True
        for w in graph[v]:
            if not visited[w]:
                dfs(w)
    components = 0
    for node in graph['nodes']:
        if not visited[node]:
            dfs(node)
            components += 1
    return components

def girvan_newman(graph):
    while connected_components(graph) < 4:
        betweenness = edge_betweenness(graph)
        edge_to_remove = max(betweenness, key=betweenness.get)
        remove_edge(graph, edge_to_remove)
    return graph

def print_graph(graph):
    # Find connected components (communities)
    visited = {node: False for node in graph['nodes']}
    communities = []
    
    def dfs(v, community):
        visited[v] = True
        community.append(v)
        for w in graph[v]:
            if not visited[w]:
                dfs(w, community)
    
    for node in graph['nodes']:
        if not visited[node]:
            community = []
            dfs(node, community)
            communities.append(community)
    
    # Print communities
    print("Communities:")
    for i, community in enumerate(communities, 1):
        print(f"Community {i}: {community}")
    
    # Print remaining edges
    print("\nRemaining edges:")
    for edge in graph['edges']:
        print(edge)


graph = {
    'nodes': [0, 1, 2, 3, 4, 5, 6],
    'edges': [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6)],
    0: [1, 2],
    1: [0, 2, 3],
    2: [0, 1, 3, 4],
    3: [1, 2, 4, 5],
    4: [2, 3, 5, 6],
    5: [3, 4, 6],
    6: [4, 5]
}

graph2 = {
    'nodes': [0, 1, 2, 3, 4, 5, 6, 7, 8],
    'edges': [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (6, 7), (7, 8), (8, 6)],
    0: [1, 2],
    1: [0, 2, 3],
    2: [0, 1, 3, 4],
    3: [1, 2, 4, 5],
    4: [2, 3, 5, 6],
    5: [3, 4, 6],
    6: [4, 5, 7, 8],
    7: [6, 8],
    8: [6, 7]
}

graph3 = {
    'nodes': [0, 1, 2, 3, 4, 5, 6, 7],
    'edges': [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (6, 7)],
    0: [1, 2],
    1: [0, 2, 3],
    2: [0, 1, 3, 4],
    3: [1, 2, 4, 5],
    4: [2, 3, 5, 6],
    5: [3, 4, 6],
    6: [4, 5, 7],
    7: [6]
}

result = girvan_newman(graph3)
print_graph(result)