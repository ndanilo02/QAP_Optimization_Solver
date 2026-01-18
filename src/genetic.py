import random
import copy
import time
import numpy as np

class Individual:
    """
    Ovo je jedna jedinka (jedno moguce resenje).
    'code' nam je niz brojeva koji kaze gde ide koja fabrika.
    'cost' je cena tog rasporeda (gledamo da bude sto manja).
    """
    def __init__(self, n, flow, distance, code=None):
        self.flow = flow
        self.distance = distance
        self.n = n
        
        # Ako nismo dobili gotov kod, pravimo nasumican raspored
        if code is None:
            self.code = list(range(n))
            random.shuffle(self.code)
        else:
            self.code = code
            
        self.cost = 0
        self.calc_cost()

    def calc_cost(self):
        """Racuna koliko kosta ovaj raspored (mnozi protok i rastojanje)."""
        self.cost = 0
        for i in range(self.n):
            for j in range(self.n):
                loc_i = self.code[i] # Gde se nalazi prva fabrika
                loc_j = self.code[j] # Gde se nalazi druga fabrika
                # Dodajemo cenu: protok izmedju fabrika * rastojanje izmedju lokacija
                self.cost += self.flow[i][j] * self.distance[loc_i][loc_j]

def selection(population, k):
    """Bira jednog roditelja tako sto uzme k nasumicnih i pobedjuje onaj sa najmanjom cenom."""
    k = min(len(population), k)
    participants = random.sample(population, k)
    # Vracamo onog koji je 'najjeftiniji'
    return min(participants, key=lambda x: x.cost)

def crossover(parent1, parent2, child1, child2):
    """
    OX1 Ukrstanje.
    Pravi decu tako sto uzme deo gena od prvog roditelja, 
    a ostatak popuni iz drugog roditelja (pazeci da se brojevi ne ponove).
    """
    n = len(parent1.code)
    
    # Pomocna funkcija koja radi samo ukrstanje
    def apply_ox(p1_code, p2_code):
        new_code = [-1] * n
        # Biramo dve tacke za secenje
        start, end = sorted(random.sample(range(n), 2))
        
        # Prepisujemo srednji deo od prvog roditelja
        new_code[start:end+1] = p1_code[start:end+1]
        
        # Ostalo popunjavamo redom iz drugog roditelja
        current_pos = (end + 1) % n
        p2_pos = (end + 1) % n
        
        while -1 in new_code:
            candidate = p2_code[p2_pos]
            # Ubacujemo broj samo ako vec ne postoji u detetu
            if candidate not in new_code:
                new_code[current_pos] = candidate
                current_pos = (current_pos + 1) % n
            p2_pos = (p2_pos + 1) % n
        return new_code

    # Primenjujemo logiku na oba deteta
    child1.code = apply_ox(parent1.code, parent2.code)
    child2.code = apply_ox(parent2.code, parent1.code)

def mutation(individual, p):
    """Mutacija: Nasumicno zamenimo mesta dvema fabrikama u nizu."""
    if random.random() < p:
        n = len(individual.code)
        idx1, idx2 = random.sample(range(n), 2)
        # Zamena mesta (swap)
        individual.code[idx1], individual.code[idx2] = individual.code[idx2], individual.code[idx1]

def solve_genetic(flow, distance, max_seconds=10.0, 
                  population_size=100, tournament_size=10, 
                  mutation_prob=0.05, elitism_size=20):
    """
    Glavna funkcija koja vrti evoluciju dok ne istekne vreme.
    """
    n = len(flow)
    
    # Pravimo pocetnu populaciju (nasumicna resenja)
    population = [Individual(n, flow, distance) for _ in range(population_size)]
    new_population = [Individual(n, flow, distance) for _ in range(population_size)]
    
    # Namestamo da broj elita bude paran zbog lakseg kopiranja
    if (population_size - elitism_size) % 2 != 0:
        elitism_size += 1
        
    start_time = time.time()
    generation = 0
    history = [] # Ovde pamtimo najbolju cenu kroz vreme za grafik
    
    best_global_cost = float('inf')
    best_global_code = None

    while (time.time() - start_time) < max_seconds:
        # Sortiramo populaciju: najbolji (najmanja cena) idu na pocetak liste
        population.sort(key=lambda x: x.cost)
        
        # Pamtimo najbolje resenje ikad nadjeno
        current_best = population[0]
        if current_best.cost < best_global_cost:
            best_global_cost = current_best.cost
            best_global_code = list(current_best.code)
            
        history.append(best_global_cost)

        # 1. ELITIZAM: Najbolji prezivljavaju bez izmena
        for i in range(elitism_size):
            new_population[i] = copy.deepcopy(population[i])
            
        # 2. OSTALI SE STVARAJU UKRSTANJEM
        for i in range(elitism_size, population_size, 2):
            # Biramo dva roditelja turnirom
            parent1 = selection(population, tournament_size)
            parent2 = selection(population, tournament_size)
            
            # Pravimo kopije da bi bile deca
            new_population[i] = copy.deepcopy(parent1)
            new_population[i+1] = copy.deepcopy(parent2)
            
            # Ukrstamo ih
            crossover(parent1, parent2, new_population[i], new_population[i+1])
            
            # Malo ih izmenimo (mutacija)
            mutation(new_population[i], mutation_prob)
            mutation(new_population[i+1], mutation_prob)
            
            # Moramo ponovo da izracunamo cenu jer smo im promenili raspored
            new_population[i].calc_cost()
            new_population[i+1].calc_cost()
            
        # Nova populacija postaje trenutna
        population = copy.deepcopy(new_population)
        generation += 1

    total_time = time.time() - start_time
    return best_global_code, best_global_cost, total_time, generation, history