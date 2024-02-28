from graph import Graph
import sys

def pagerank(graph, iters=10000, d=0.01):
    length = len(graph.adj)
    pr = [1 / length] * length

    for _ in range(iters):
        newPr = [0] * length
        for i in range(length):
            for j in graph.adj[i]:
                newPr[j] += d * pr[i] / len(graph.adj[i])
        for i in range(length):
            newPr[i] += (1-d) / length
        pr = newPr
    return pr


if __name__ == "__main__":
    G = Graph()
    G.readgraph(sys.argv[1])

    scores = pagerank(G)

    top10 = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:10]

    print("Top 10 nodes: ", end="")
    for i in top10:
        print(f"{i}, ", end = "")