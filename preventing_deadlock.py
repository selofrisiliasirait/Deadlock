# preventing_deadlock.py
import threading
import time

# dua "resource" sebagai Lock, berurutan: 0, 1
resources = [threading.Lock(), threading.Lock()]

def process(name, want):
    # want = list of resource indices the process needs (e.g., [0,1])
    print(f"{name} ingin {want}")
    # PREVENTION: acquire locks in ascending order (global ordering)
    for r in sorted(want):
        print(f"{name} mencoba mengambil resource {r}")
        resources[r].acquire()
        print(f"{name} memegang resource {r}")
        time.sleep(0.2)  # simulasi kerja
    print(f"{name} melakukan pekerjaan kritis")
    time.sleep(0.5)
    # release in reverse (baik untuk kebiasaan)
    for r in reversed(sorted(want)):
        resources[r].release()
        print(f"{name} melepaskan resource {r}")

# contoh: dua process yang masing2 butuh [0,1]
t1 = threading.Thread(target=process, args=("P1",[0,1]))
t2 = threading.Thread(target=process, args=("P2",[0,1]))

t1.start(); t2.start()
t1.join(); t2.join()
print("Selesai — tidak terjadi deadlock karena urutan penguncian sama.")
