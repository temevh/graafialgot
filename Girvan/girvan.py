import sys

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
    
    print("Communities:")
    for i, community in enumerate(communities, 1):
        print(f"Community {i}: {community}")

    print("\nRemaining edges:")
    for edge in graph['edges']:
        print(edge)

def readGraph(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    graph = {}
    nodes = []
    edges = []

    for line in lines:
        node_and_adjacents = list(map(int, line.split()))
        node = node_and_adjacents[0]
        adjacents = node_and_adjacents[1:]

        nodes.append(node)
        graph[node] = adjacents

        for adjacent in adjacents:
            edge = tuple(sorted((node, adjacent)))
            if edge not in edges:
                edges.append(edge)

    graph['nodes'] = nodes
    graph['edges'] = edges

    return graph

inputgraph = sys.argv[1]
graph = readGraph(inputgraph)
result = girvan_newman(graph)
print_graph(result)