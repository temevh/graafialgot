class Graph:
    def __init__(self, n=None) -> None:
        if n is None:
            self.n = 0
            self.adj = []
            self.w = {}
            self.communities = {}
        else:
            self.n = n
            self.adj = [[] for i in range(self.n)]
            self.w = {}
            self.communities = {i: [i] for i in range(self.n)}

    def calculate_modularity(self):
    # This is a placeholder implementation. You'll need to replace this with
    # your actual modularity calculation.
        m = sum(self.w.values())
        q = 0.0
        for i in range(self.n):
            ki = sum(self.w.get((i, j), 0) for j in self.adj[i])
            for j in self.adj[i]:
                kj = sum(self.w.get((j, k), 0) for k in self.adj[j])
                if self.communities[i] == self.communities[j]:
                    q += self.w.get((i, j), 0) - ki * kj / (2.0 * m)
        return q / (2.0 * m)

    def optimize_modularity(self):
        for i in range(self.n):
            best_community = self.communities[i]
            best_gain = 0
            for j in self.adj[i]:
                original_community = self.communities[j]
                self.communities[j] = self.communities[i]
                gain = self.calculate_modularity() - self.calculate_modularity()
                if gain > best_gain:
                    best_community = self.communities[i]
                    best_gain = gain
                self.communities[j] = original_community
            self.communities[i] = best_community

    def form_new_network(self):
    # Implement new network formation here
        new_adj = {}
        new_w = {}
        for i in range(self.n):
            for j in self.adj[i]:
                if self.communities[i] != self.communities[j]:
                    if (self.communities[i], self.communities[j]) not in new_w:
                        new_w[(self.communities[i], self.communities[j])] = self.w.get((i, j), 0)
                    else:
                        new_w[(self.communities[i], self.communities[j])] += self.w.get((i, j), 0)
                    new_adj.setdefault(self.communities[i], []).append(self.communities[j])
        self.adj = [new_adj.get(i, []) for i in range(self.n)]
        self.w = new_w
        self.communities = {i: [i] for i in range(self.n)}

    def louvain_method(self):
        while True:
            initial_modularity = self.calculate_modularity()
            self.optimize_modularity()
            self.form_new_network()
            if self.calculate_modularity() <= initial_modularity:
                break
  

    def addEdge(self, u: int, v: int, w = None) -> None:
        nn = self.n
        self.n = max(u+1,v+1, self.n)
        self.adj.extend([[] for i in range(self.n - nn)])
        self.adj[u].append(v)
        if w is not None:
            self.w[(u,v)] = w
  
    def readgraph(self, filename: str) -> None:
        f = open(filename, 'r')
        for line in f:
            line = line.strip().split()
            if len(line) >= 2:
                u = int(line[0])
                if u >= self.n:
                    self.adj.extend([[] for i in range(u + 1 - self.n)])
                    self.communities.update({i: [i] for i in range(self.n, u + 1)})
                    self.n = u + 1
                for i in range(1, len(line)):
                    v = int(line[i])
                    self.addEdge(u, v)  # Assuming unweighted graph
        f.close()
    
U = Graph()
U.readgraph("testgraph.txt")
U.louvain_method()