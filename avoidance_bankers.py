# avoidance_bankers.py
# Contoh kecil Banker's algorithm untuk 3 proses dan 3 unit resource tunggal jenis sama
def is_safe(available, max_demand, allocation):
    n = len(max_demand)
    work = available
    finish = [False]*n
    while True:
        progressed = False
        for i in range(n):
            if not finish[i]:
                need = max_demand[i] - allocation[i]
                if need <= work:
                    work += allocation[i]
                    finish[i] = True 
                    progressed = True
        if not progressed:
            break
    return all(finish)

# state awal
available = 3
max_demand = [2,2,2]
allocation = [0,0,0]

def request(pid, req):
    global available, allocation
    print(f"Process {pid} meminta {req}. Available sebelum: {available}")
    if req > available:
        print("Tolak: tidak cukup resource tersedia.")
        return False
    # coba alokasi sementara
    available -= req
    allocation[pid] += req
    safe = is_safe(available, max_demand, allocation)
    if safe:
        print("Dipenuhi — sistem tetap safe.")
        return True
    else:
        # rollback
        available += req
        allocation[pid] -= req
        print("Tolak: alokasi akan membuat sistem unsafe (menghindari deadlock).")
        return False

# Simulasi:
request(0, 2)   # P0 dapat 2
request(1, 2)   # P1 dapat 2 -> mungkin ditolak tergantung state
request(2, 2)   # P2 mencoba
print("State akhir: available=", available, "allocation=", allocation)
