import time
import random
from utils import calculate_cost, delta_cost
from local_search import run_local_search_2opt

def ox_crossover(p1, p2):
    n = len(p1)
    start, end = sorted(random.sample(range(n), 2))
    
    child = [-1] * n
    child[start:end] = p1[start:end]
    
    used = set(child[start:end])
    
    pos = end
    for gene in p2[end:] + p2[:end]:
        if gene not in used:
            if pos >= n:
                pos = 0
            child[pos] = gene
            pos += 1
            
    return child

def mutate(perm, mutation_type='swap'):
    n = len(perm)
    mutated = list(perm)
    
    if mutation_type == 'swap':
        i, j = random.sample(range(n), 2)
        mutated[i], mutated[j] = mutated[j], mutated[i]
        
    elif mutation_type == 'inversion':
        i, j = sorted(random.sample(range(n), 2))
        mutated[i:j+1] = reversed(mutated[i:j+1])
        
    elif mutation_type == 'scramble':
        i, j = sorted(random.sample(range(n), 2))
        sub = mutated[i:j+1]
        random.shuffle(sub)
        mutated[i:j+1] = sub
        
    return mutated

def solve_genetic(flow, dist, max_seconds=30, max_stagnation=1000, 
                  population_size=100, tournament_size=5, 
                  base_mutation_prob=0.15, elitism_size=2,
                  ls_prob=0.05, ls_max_seconds=0.05):
    n = len(flow)
    start_time = time.time()
    
    population = []
    for _ in range(population_size):
        perm = list(range(n))
        random.shuffle(perm)
        cost = calculate_cost(flow, dist, perm)
        population.append((perm, cost))
        
    population.sort(key=lambda x: x[1])
    
    best_perm = list(population[0][0])
    best_cost = population[0][1]
    
    history_cost = [best_cost]
    generation = 0
    no_improvement_counter = 0
    
    best_perm, best_cost = run_local_search_2opt(flow, dist, best_perm, max_seconds=0.5)
    population[0] = (best_perm, best_cost)
    population.sort(key=lambda x: x[1])
    
    while (time.time() - start_time) < max_seconds:
        generation += 1
        
        stagnation_ratio = no_improvement_counter / max_stagnation
        current_mutation_prob = base_mutation_prob + (0.5 - base_mutation_prob) * stagnation_ratio
        
        if stagnation_ratio < 0.3:
            mutation_type = 'swap'
        elif stagnation_ratio < 0.7:
            mutation_type = 'inversion'
        else:
            mutation_type = 'scramble'
            
        if no_improvement_counter > 0 and no_improvement_counter % int(max_stagnation * 0.8) == 0:
            keep_size = max(1, int(population_size * 0.1))
            preserved = population[:keep_size]
            
            regenerated = []
            for _ in range(population_size - keep_size):
                perm = list(range(n))
                random.shuffle(perm)
                cost = calculate_cost(flow, dist, perm)
                if random.random() < 0.1:
                    perm, cost = run_local_search_2opt(flow, dist, perm, max_seconds=0.02)
                regenerated.append((perm, cost))
                
            population = preserved + regenerated
            population.sort(key=lambda x: x[1])
            no_improvement_counter += 1
            continue

        if no_improvement_counter >= max_stagnation:
            print(f"   -> [STOP] Stagnacija od {max_stagnation} generacija.")
            break
            
        new_population = []
        
        for i in range(elitism_size):
            new_population.append((list(population[i][0]), population[i][1]))
            
        while len(new_population) < population_size:
            p1_perm = min(random.sample(population, tournament_size), key=lambda x: x[1])[0]
            p2_perm = min(random.sample(population, tournament_size), key=lambda x: x[1])[0]
            
            child_perm = ox_crossover(p1_perm, p2_perm)
            child_cost = calculate_cost(flow, dist, child_perm)
            
            if random.random() < current_mutation_prob:
                if mutation_type == 'swap':
                    i, j = random.sample(range(n), 2)
                    delta = delta_cost(flow, dist, child_perm, i, j)
                    child_perm[i], child_perm[j] = child_perm[j], child_perm[i]
                    child_cost += delta
                else:
                    child_perm = mutate(child_perm, mutation_type)
                    child_cost = calculate_cost(flow, dist, child_perm)
            
            if random.random() < ls_prob:
                child_perm, child_cost = run_local_search_2opt(flow, dist, child_perm, max_seconds=ls_max_seconds)
                
            new_population.append((child_perm, child_cost))
            
        population = new_population
        population.sort(key=lambda x: x[1])
        
        if population[0][1] < best_cost:
            polished_perm, polished_cost = run_local_search_2opt(flow, dist, population[0][0], max_seconds=0.2)
            if polished_cost < population[0][1]:
                population[0] = (polished_perm, polished_cost)
                population.sort(key=lambda x: x[1])
                
            best_perm = list(population[0][0])
            best_cost = population[0][1]
            no_improvement_counter = 0
        else:
            no_improvement_counter += 1
            
        history_cost.append(best_cost)
        
    elapsed_time = time.time() - start_time
    return best_perm, best_cost, elapsed_time, generation, history_cost