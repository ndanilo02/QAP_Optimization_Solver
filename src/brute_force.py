import time
import itertools
from utils import calculate_cost

def solve_brute_force(flow, dist):
    n = len(flow)
    indices = list(range(n))
    
    best_cost = float('inf')
    best_perm = None
    
    start_time = time.time()
    
    for perm in itertools.permutations(indices):
        current_cost = calculate_cost(flow, dist, perm)
        
        if current_cost < best_cost:
            best_cost = current_cost
            best_perm = perm
            
    elapsed_time = time.time() - start_time
    return best_perm, best_cost, elapsed_time