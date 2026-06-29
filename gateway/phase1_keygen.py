import oqs
import hashlib
import time
import tracemalloc

def gateway_phase1():
    print("=== Gateway Phase 1: ML-KEM-768 ===")

    # قياس RAM
    tracemalloc.start()

    # قياس الوقت
    start = time.perf_counter()

    # ML-KEM-768 keygen
    kem = oqs.KeyEncapsulation('ML-KEM-768')
    public_key = kem.generate_keypair()

    # Encapsulation
    ciphertext, shared_secret = kem.encap_secret(public_key)

    # Session key
    session_key = hashlib.sha256(shared_secret).digest()

    end = time.perf_counter()

    # RAM reading
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # النتايج
    latency_ms = (end - start) * 1000
    ram_kb = peak / 1024

    print(f"Latency:     {latency_ms:.2f} ms  (baseline: 51.3 ms)")
    print(f"RAM (peak):  {ram_kb:.2f} KB  (baseline: 34.2 KB)")
    print(f"Ciphertext:  {len(ciphertext)} bytes")
    print(f"Session key: {session_key.hex()[:16]}...")

    return session_key, ciphertext

if __name__ == "__main__":
    gateway_phase1()
