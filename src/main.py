import os
import time
import matplotlib.pyplot as plt
from utils import load_qap_data, get_bks_for_file
from brute_force import solve_brute_force
from genetic import solve_genetic

def main():
    input_file = "lipa60a.dat"  
    
    POP_SIZE = 100
    ELITISM = 4
    TOURNAMENT = 5
    BASE_MUTATION = 0.15
    LS_PROB = 0.10
    LS_MAX_TIME = 0.02
    
    MAX_TIME = 15.0
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', input_file)
    print(f"============================================================")
    print(f"[START] POKRETANJE QAP OPTIMIZACIJE: {input_file}")
    print(f"============================================================")
    
    n, flow, dist = load_qap_data(file_path)
    if n is None: 
        return
    
    print(f"Dimenzija problema: N = {n}")

    PATIENCE = int((n * n) * 1.2) + 200
    print(f"-> Maksimalna stagnacija: {PATIENCE} generacija")

    bks_value = get_bks_for_file(input_file)
    if bks_value is not None:
        print(f"-> Poznato optimalno resenje iz literature: {bks_value}")
    else:
        print("-> Optimalno resenje za ovu instancu nije u nasoj bazi literature.")

    bf_cost = None
    if n < 11:
        print("\n[1] Pokretanje Brute-Force algoritma...")
        bf_perm, bf_cost, bf_time, bf_completed = solve_brute_force(flow, dist, max_seconds=10.0)
        if bf_completed:
            print(f"    -> Pronadjen optimum: {bf_cost} (Vreme: {bf_time:.4f}s)")
        else:
            print(f"    -> Prekinuto zbog vremenskog limita! Najbolja cena: {bf_cost}")
    else:
        print(f"\n[1] Brute-Force je preskocen (N={n} > 10).")

    print(f"\n[2] Pokretanje Memetskog Genetskog Algoritma...")
    
    ga_perm, ga_cost, ga_time, gens, history = solve_genetic(
        flow, dist,
        max_seconds=MAX_TIME,
        max_stagnation=PATIENCE,
        population_size=POP_SIZE,
        tournament_size=TOURNAMENT,
        base_mutation_prob=BASE_MUTATION,
        elitism_size=ELITISM,
        ls_prob=LS_PROB,
        ls_max_seconds=LS_MAX_TIME
    )
    
    print(f"    -> Rezultat GA: {ga_cost}")
    print(f"    -> Ukupno generacija: {gens}")
    print(f"    -> Vreme izvrsavanja: {ga_time:.2f}s")

    print(f"\n============================================================")
    print(f"[REZULTATI] REZULTATI I ANALIZA")
    print(f"============================================================")
    
    target_value = bf_cost if bf_cost is not None else bks_value
    
    if target_value is not None:
        gap = (ga_cost - target_value) / target_value * 100
        print(f"Dobijena cena:   {ga_cost}")
        print(f"Ciljna vrednost: {target_value}")
        print(f"Odstupanje:      {gap:.3f}%")
        if gap == 0:
            print("[OK] SAVRSENO! Pronadjeno je globalno optimalno resenje.")
        elif gap < 1.0:
            print("[OK] Odlican rezultat! Odstupanje je manje od 1% u odnosu na optimum.")
        else:
            print(f"[INFO] Razlika u ceni iznosi {ga_cost - target_value} jedinica.")
    else:
        print(f"Dobijena cena: {ga_cost} (nema dostupnog optimuma za poredjenje).")
        
    print(f"============================================================")

    plt.figure(figsize=(10, 6))
    plt.plot(history, label="Najbolje resenje kroz generacije", color="#1f77b4", linewidth=2)
    
    if target_value is not None:
        plt.axhline(y=target_value, color='r', linestyle='--', label=f"Optimum ({target_value})")
        
    plt.title(f"Konvergencija Memetskog GA za {input_file} (N={n})", fontsize=14, fontweight='bold')
    plt.xlabel("Generacija", fontsize=12)
    plt.ylabel("Cena", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=11)
    
    results_dir = os.path.join(current_dir, '..', 'results')
    os.makedirs(results_dir, exist_ok=True)
    plot_path = os.path.join(results_dir, f"convergence_{input_file.split('.')[0]}.png")
    plt.savefig(plot_path, dpi=150)
    print(f"Grafik konvergencije sacuvan u: results/convergence_{input_file.split('.')[0]}.png\n")

if __name__ == "__main__":
    main()