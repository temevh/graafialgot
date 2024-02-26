import sys

def edge_betweenness(graph):
    # Initialize betweenness dictionary for tracking edge betweenness values
    betweenness = {edge: 0 for edge in graph['edges']}
    betweenness.update({(v, u): 0 for (u, v) in betweenness.keys()})

    # Iterate through nodes to calculate node betweenness using BFS
    for node in graph['nodes']:
        stack, paths, dist = ([], {v: [] for v in graph['nodes']},
                              {v: float('inf') for v in graph['nodes']})
        stack.append(node)
        paths[node] = [[node]]
        dist[node] = 0

        # BFS to find the shortest paths and update betweenness values
        while stack:
            vertex = stack.pop(0)
            for neighbour in graph[vertex]:

                # if distance is inf, neighbour has not been visited
                if dist[neighbour] == float('inf'):
                    stack.append(neighbour)
                    dist[neighbour] = dist[vertex] + 1

                if dist[neighbour] == dist[vertex] + 1:
                    paths[neighbour].extend([path + [neighbour] for path in paths[vertex]])

        nodeBetweenness = {edge: 0 for edge in betweenness.keys()}

        # Update betweenness values based on the shortest paths
        for path in [path for paths in paths.values() for path in paths]:

            for edge in zip(path[:-1], path[1:]):
                nodeBetweenness[edge] += 1
                nodeBetweenness[(edge[1], edge[0])] += 1  # Add this line

        for edge in betweenness.keys():
            betweenness[edge] += nodeBetweenness[edge] / 2

    return betweenness

def remove_edge(graph, edge):
    # Check if the edge exists in the graph
    if edge in graph['edges']:
        # Remove the edge from the adjacency lists of its nodes
        if edge[1] in graph[edge[0]]:
            graph[edge[0]].remove(edge[1])
        if edge[0] in graph[edge[1]]:
            graph[edge[1]].remove(edge[0])
        # Remove the edge from the list of edges
        print(f"Removing edge {edge}")
        graph['edges'].remove(edge)

def connected_components(graph):
    # Initialize all nodes as not visited
    visited = {node: False for node in graph['nodes']}
    # Depth-first search
    def dfs(v):
        visited[v] = True
        for w in graph[v]:
            if not visited[w]:
                dfs(w)
    # Count connected components
    components = 0
    for node in graph['nodes']:
        if not visited[node]:
            dfs(node)
            components += 1
    return components


def girvan_newman(graph):
    # Detecting 4 communities (ie. run the loop until we have found 4 distinct communities)
    while connected_components(graph) < 4: 
        betweenness = edge_betweenness(graph)
        edge_to_remove = max(betweenness, key=betweenness.get)
        remove_edge(graph, edge_to_remove)
    return graph

def print_graph(graph):
    visited = {node: False for node in graph['nodes']}
    communities = []
    
    # Depth-first search
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
            community.sort()
            communities.append(community)
    
    print("Communities:")
    for i, community in enumerate(communities, 1):
        print(f"Community {i}: {community}")

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
            reverseEdge = tuple((adjacent, node))

            if edge not in edges:
                edges.append(edge)
                edges.append(reverseEdge)

    graph['nodes'] = nodes
    graph['edges'] = edges

    return graph

inputgraph = sys.argv[1]
graph = readGraph(inputgraph)
result = girvan_newman(graph)
print_graph(result)