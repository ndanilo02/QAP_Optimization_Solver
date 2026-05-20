import time
from utils import calculate_cost, delta_cost

def run_local_search_2opt(flow, dist, perm, max_seconds=1.0):
    n = len(flow)
    best_perm = list(perm)
    current_cost = calculate_cost(flow, dist, best_perm)
    
    start_time = time.time()
    improved = True
    
    while improved:
        improved = False
        
        for i in range(n - 1):
            for j in range(i + 1, n):
                if max_seconds and (time.time() - start_time) > max_seconds:
                    return best_perm, current_cost
                
                delta = delta_cost(flow, dist, best_perm, i, j)
                
                if delta < 0:
                    best_perm[i], best_perm[j] = best_perm[j], best_perm[i]
                    current_cost += delta
                    improved = True
                    break
            if improved:
                break
                
    return best_perm, current_cost