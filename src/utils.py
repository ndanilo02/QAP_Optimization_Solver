import numpy as np
import os

def load_qap_data(file_path):
    """
    Parsiranje QAPLIB formata.
    Vraca: n (int), flow (matrix), distance (matrix)
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read().split()
            
            # Dimenzija problema
            n = int(content[0])
            data = [int(x) for x in content[1:]]
            
            # Validacija velicine podataka
            if len(data) < 2 * n * n:
                return None, None, None

            # Izdvajanje matrica (F i D)
            flow_flat = data[0 : n*n]
            flow_matrix = np.array(flow_flat).reshape(n, n)
            
            dist_flat = data[n*n : 2*n*n]
            distance_matrix = np.array(dist_flat).reshape(n, n)
            
            return n, flow_matrix, distance_matrix

    except Exception as e:
        print(f"Greska pri ucitavanju: {e}")
        return None, None, None