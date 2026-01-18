import numpy as np
import itertools
import os
import time
from utils import load_qap_data  

def calculate_cost(permutation, flow, distance):
    """
    Cost function)
    Suma(Flow[i][j] * Distance[perm[i]][perm[j]])
    """
    n = len(permutation)
    cost = 0
    
    for i in range(n):
        for j in range(n):
            loc_i = permutation[i]
            loc_j = permutation[j]
            cost += flow[i][j] * distance[loc_i][loc_j]
            
    return cost

def solve_brute_force(flow, distance):
    """Resavanje pretragom svih permutacija."""
    n = len(flow)
    indices = list(range(n)) 
    
    best_cost = float('inf') 
    best_permutation = None
    
    # Generisanje svih mogucih rasporeda
    all_permutations = itertools.permutations(indices)
    
    start_time = time.time()
    
    for perm in all_permutations:
        current_cost = calculate_cost(perm, flow, distance)
        
        # Minimizacija cene
        if current_cost < best_cost:
            best_cost = current_cost
            best_permutation = perm
        
    end_time = time.time()
    
    return best_permutation, best_cost, end_time - start_time

# Unit test
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'test_input.txt')
    
    n, flow, dist = load_qap_data(file_path)
    
    if n is not None:
        best_p, best_c, duration = solve_brute_force(flow, dist)
        print(f"BF Rezultat: {best_c} ({duration:.4f}s)")