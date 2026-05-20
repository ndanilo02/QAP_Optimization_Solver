import os
import json

def load_qap_data(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read().split()
            
            if not content:
                return None, None, None
                
            n = int(content[0])
            data = [int(float(x)) for x in content[1:]]
            
            if len(data) < 2 * n * n:
                print("Greska: Fajl je ostecen ili nepotpun.")
                return None, None, None

            flow_matrix = []
            for i in range(n):
                flow_matrix.append(data[i*n : (i+1)*n])
                
            dist_offset = n * n
            distance_matrix = []
            for i in range(n):
                distance_matrix.append(data[dist_offset + i*n : dist_offset + (i+1)*n])
            
            return n, flow_matrix, distance_matrix

    except Exception as e:
        print(f"Greska pri ucitavanju fajla: {e}")
        return None, None, None

def calculate_cost(flow, dist, perm):
    n = len(perm)
    cost = 0
    for i in range(n):
        for j in range(n):
            cost += flow[i][j] * dist[perm[i]][perm[j]]
    return cost

def delta_cost(flow, dist, perm, r, s):
    if r == s:
        return 0
        
    n = len(perm)
    d = 0
    
    d += (flow[r][r] - flow[s][s]) * (dist[perm[s]][perm[s]] - dist[perm[r]][perm[r]])
    d += (flow[r][s] - flow[s][r]) * (dist[perm[s]][perm[r]] - dist[perm[r]][perm[s]])
    
    for k in range(n):
        if k != r and k != s:
            d += (flow[r][k] - flow[s][k]) * (dist[perm[s]][perm[k]] - dist[perm[r]][perm[k]])
            d += (flow[k][r] - flow[k][s]) * (dist[perm[k]][perm[s]] - dist[perm[k]][perm[r]])
            
    return d

def get_bks_for_file(filename):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, '..', 'data', 'qaplib_solutions.json')
        
        if not os.path.exists(json_path):
            return None
            
        with open(json_path, 'r') as f:
            bks_data = json.load(f)
            
        key = filename.lower().replace(".dat", "").replace(".txt", "")
        return bks_data.get(key, None)
    except Exception:
        return None