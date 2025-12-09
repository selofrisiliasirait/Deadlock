# detection_deadlock.py
# Simulasi Allocation & Request untuk 4 proses dan beberapa resource
# allocation[i] = list of resources held by Pi
# request[i] = list of resources Pi is currently waiting for

allocation = {
    'P1': {'R1'},
    'P2': {'R2'},
    'P3': {'R3'},
    'P4': set()
}
request = {
    'P1': {'R2'},   # P1 menunggu R2 (dipegang P2)
    'P2': {'R3'},   # P2 menunggu R3 (dipegang P3)
    'P3': {'R1'},   # P3 menunggu R1 (dipegang P1) -> siklus P1->P2->P3->P1
    'P4': {'R1'}
}

# Bangun wait-for graph: edge Pi -> Pj jika Pi menunggu resource yg dipegang Pj
def build_wait_for(allocation, request):
    who_holds = {}
    for p,res_set in allocation.items():
        for r in res_set:
            who_holds[r] = p
    graph = {p:set() for p in allocation}
    for p, reqs in request.items():
        for r in reqs:
            holder = who_holds.get(r)
            if holder and holder != p:
                graph[p].add(holder)
    return graph

def detect_cycle(graph):
    visited = set()
    stack = set()
    path = []

    def dfs(u):
        visited.add(u)
        stack.add(u)
        path.append(u)
        for v in graph[u]:
            if v not in visited:
                if dfs(v):
                    return True
            elif v in stack:
                # found cycle, extract it
                cycle = path[path.index(v):] + [v]
                print("Deadlock terdeteksi! Siklus:", " -> ".join(cycle))
                return True
        stack.remove(u)
        path.pop()
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    print("Tidak ada deadlock terdeteksi.")
    return False

g = build_wait_for(allocation, request)
print("Wait-for graph:", g)
detect_cycle(g)

