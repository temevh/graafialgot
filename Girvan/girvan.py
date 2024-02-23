import sys

def edge_betweenness(graph):
    # Initialize betweenness for each edge as 0
    betweenness = {edge: 0 for edge in graph['edges']}
    # Add reverse edges to the betweenness dictionary
    betweenness.update({(v, u): 0 for (u, v) in betweenness.keys()})
    # For each node in the graph
    for node in graph['nodes']:
        # Initialize stack, paths, and distance
        stack, paths, dist = [], {v: [] for v in graph['nodes']}, {v: float('inf') for v in graph['nodes']}
        # Start from the current node
        stack.append(node)
        paths[node] = [[node]]
        dist[node] = 0
        # While there are nodes to process
        while stack:
            v = stack.pop(0)
            # For each neighbor of the current node
            for w in graph[v]:
                # If the neighbor hasn't been visited yet
                if dist[w] == float('inf'):
                    # Add it to the stack and update its distance
                    stack.append(w)
                    dist[w] = dist[v] + 1
                # If the shortest path to the neighbor has been found
                if dist[w] == dist[v] + 1:
                    # Add all paths to the neighbor
                    paths[w].extend([path + [w] for path in paths[v]])
        # Calculate betweenness for each edge
        node_betweenness = {edge: 0 for edge in betweenness.keys()}
        for path in [path for paths in paths.values() for path in paths]:
            for edge in zip(path[:-1], path[1:]):
                # Only update betweenness if the edge exists in the graph
                if edge in betweenness:
                    node_betweenness[edge] += 1
        # Update the betweenness of each edge
        for edge in betweenness.keys():
            betweenness[edge] += node_betweenness[edge] / 2
    # Return the betweenness of each edge
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
        # Remove the edge from the betweenness dictionary
        del betweenness[edge_to_remove]
        del betweenness[(edge_to_remove[1], edge_to_remove[0])]  # remove the reverse edge as well
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
            if edge not in edges:
                edges.append(edge)

    graph['nodes'] = nodes
    graph['edges'] = edges

    return graph

inputgraph = sys.argv[1]
graph = readGraph(inputgraph)
result = girvan_newman(graph)
print_graph(result)