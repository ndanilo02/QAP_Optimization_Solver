import os
import time
import matplotlib.pyplot as plt
from utils import load_qap_data
from brute_force import solve_brute_force
from genetic import solve_genetic

def main():
    # --- PODESAVANJA ---
    input_file = "test_n7.dat" 
    BRUTE_FORCE_LIMIT = 10 # Do koje velicine smemo da pustimo sporu pretragu
    
    # Parametri za genetski 
    POP_SIZE = 100
    TOURNAMENT = 10
    MUTATION = 0.1 
    ELITISM = 20

    # --- UCITAVANJE PODATAKA ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', input_file)
    
    print(f"--- QAP OPTIMIZACIJA ---")
    print(f"Radim sa fajlom: {input_file}")
    
    n, flow, dist = load_qap_data(file_path)
    
    if n is None:
        print("Greska: Nisam uspeo da ucitam fajl.")
        return

    print(f"Velicina problema: N = {n}")

    # --- 1. BRUTE FORCE (Samo ako je problem mali) ---
    bf_cost = None
    if n <= BRUTE_FORCE_LIMIT:
        print(f"\n[1] Pokrecem sporu pretragu (Brute Force)...")
        bf_perm, bf_cost, bf_time = solve_brute_force(flow, dist)
        print(f"   -> BF Nasao cenu: {bf_cost} (Trajalo: {bf_time:.4f}s)")
    else:
        print(f"\n[1] Preskacem sporu pretragu (Problem je prevelik).")

    # --- 2. GENETSKI ALGORITAM ---
    print(f"\n[2] Pokrecem Genetski Algoritam...")
    
    # Ako je mali problem dajemo mu 3 sekunde, ako je veliki 30
    max_time = 3.0 if n < 15 else 30.0
    
    ga_perm, ga_cost, ga_time, generations, history = solve_genetic(
        flow, dist, 
        max_seconds=max_time,
        population_size=POP_SIZE,
        tournament_size=TOURNAMENT,
        mutation_prob=MUTATION,
        elitism_size=ELITISM
    )
    
    print(f"   -> GA Nasao cenu: {ga_cost}")
    print(f"   -> Broj generacija: {generations}")
    print(f"   -> Vreme: {ga_time:.4f} sec")

    # --- 3. POREDJENJE ---
    print("\n--- REZULTAT ---")
    if bf_cost is not None:
        if ga_cost == bf_cost:
            print("✅ Super! Genetski je nasao isto sto i spora pretraga.")
        else:
            diff = ga_cost - bf_cost
            print(f"⚠️ Nije bas idealno. Razlika je: {diff}")
    else:
        print(f"Zavrseno. Najbolja cena: {ga_cost}")

    # --- 4. CRTANJE GRAFIKA ---
    plt.figure(figsize=(10, 6))
    plt.plot(history, label='Najbolja cena')
    plt.title(f'Kako se popravljalo resenje kroz vreme (N={n})')
    plt.xlabel('Generacija')
    plt.ylabel('Cena')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    results_path = os.path.join(current_dir, '..', 'results', f'convergence_n{n}.png')
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    
    plt.savefig(results_path)
    print(f"\nGrafik sacuvan ovde: {results_path}")
    plt.show()

if __name__ == "__main__":
    main()