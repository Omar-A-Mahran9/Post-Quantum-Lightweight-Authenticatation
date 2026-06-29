import oqs
import hashlib
import time
import tracemalloc
from Crypto.Cipher import ChaCha20_Poly1305

def full_ophl_simulation(num_messages=100):
    print("=== OPHL Full Simulation ===\n")
    
    # Phase 1
    tracemalloc.start()
    start = time.perf_counter()
    
    kem = oqs.KeyEncapsulation('ML-KEM-768')
    public_key = kem.generate_keypair()
    ciphertext, shared_secret = kem.encap_secret(public_key)
    session_key = hashlib.sha256(shared_secret).digest()
    
    phase1_time = (time.perf_counter() - start) * 1000
    _, phase1_ram = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"Phase 1 (Handshake):")
    print(f"  Latency:  {phase1_time:.2f} ms")
    print(f"  RAM:      {phase1_ram/1024:.2f} KB\n")
    
    # Phase 2
    tracemalloc.start()
    start = time.perf_counter()
    
    for i in range(num_messages):
        nonce = (i).to_bytes(12, 'big')
        cipher = ChaCha20_Poly1305.new(key=session_key, nonce=nonce)
        data = f"sensor_data_{i}".encode()
        ciphertext_msg, tag = cipher.encrypt_and_digest(data)
    
    phase2_time = (time.perf_counter() - start) * 1000
    _, phase2_ram = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"Phase 2 ({num_messages} messages):")
    print(f"  Total time: {phase2_time:.2f} ms")
    print(f"  Per message: {phase2_time/num_messages:.4f} ms")
    print(f"  RAM:        {phase2_ram/1024:.2f} KB")
    print(f"\nPQC overhead: {phase1_time/(phase1_time+phase2_time)*100:.4f}% of total runtime")

if __name__ == "__main__":
    full_ophl_simulation()
