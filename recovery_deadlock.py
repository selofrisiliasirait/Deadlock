# recovery_deadlock.py
# Kita gunakan model yang mirip detection_deadlock.py tapi menambahkan recovery step.

allocation = {
    'P1': {'R1'},
    'P2': {'R2'},
    'P3': {'R3'},
}
request = {
    'P1': {'R2'},
    'P2': {'R3'},
    'P3': {'R1'},
}

# sederhana: cost untuk meng-kill tiap process
cost = {'P1': 10, 'P2': 5, 'P3': 7}  # pilih korban berbiaya paling kecil

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

# copy dari detection
def detect_cycle_and_get_nodes(graph):
    visited = set()
    stack = []
    onstack = set()
    found_cycles = []

    def dfs(u):
        visited.add(u)
        stack.append(u); onstack.add(u)
        for v in graph[u]:
            if v not in visited:
                dfs(v)
            elif v in onstack:
                cycle = stack[stack.index(v):] + [v]
                found_cycles.append(cycle)
        stack.pop(); onstack.remove(u)

    for node in graph:
        if node not in visited:
            dfs(node)
    return found_cycles

def recover(allocation, request, cost):
    graph = build_wait_for(allocation, request)
    cycles = detect_cycle_and_get_nodes(graph)
    if not cycles:
        print("Tidak ada deadlock.")
        return
    print("Deadlock cycles found:", cycles)
    # sederhana: ambil semua proses yang terlibat dalam cycle (gabung semua cycle)
    involved = set().union(*[set(c[:-1]) for c in cycles])  # exclude repeated last node
    # pilih korban berdasarkan biaya minimal
    victim = min(involved, key=lambda p: cost.get(p, float('inf')))
    print(f"Pilih korban: {victim} (cost={cost[victim]}) — akan dipreempt / dihentikan.")
    # Recovery action: release resources held oleh victim
    released = allocation.pop(victim, set())
    # hapus permintaan victim
    request.pop(victim, None)
    # berikan resource released menjadi "available" dan coba alokasi ke processes lain yang menunggu (sederhana: lepaskan holder mapping)
    print(f"Resources yang dilepas: {released}")
    # update: siapa yang menunggu resource itu, kita anggap mereka sekarang bebas meminta ulang (di real system harus retry)
    # Untuk demo: remove edges to victim in wait-for
    for p in list(request.keys()):
        request[p] = {r for r in request[p] if r not in released}
    print("State setelah recovery — allocation:", allocation, "request:", request)
    # cek lagi
    g2 = build_wait_for(allocation, request)
    print("Wait-for graph setelah recovery:", g2)
    cycles_after = detect_cycle_and_get_nodes(g2)
    if not cycles_after:
        print("Deadlock teratasi.")
    else:
        print("Masih ada cycle:", cycles_after)

recover(allocation, request, cost)
