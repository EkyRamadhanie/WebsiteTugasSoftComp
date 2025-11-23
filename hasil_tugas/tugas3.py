import numpy as np
import pandas as pd
import random

def tsp_genetic_algorithm(cities, distance_matrix, pop_size=50, generations=100, 
                          tournament_k=5, crossover_rate=0.9, mutation_rate=0.2, elite_size=1):
    """
    Travelling Salesman Problem (TSP) dengan Genetic Algorithm
    
    Args:
        cities: List nama kota
        distance_matrix: Matrix jarak antar kota (2D list/numpy array)
        pop_size: Ukuran populasi
        generations: Jumlah generasi
        tournament_k: Ukuran tournament selection
        crossover_rate: Probabilitas crossover
        mutation_rate: Probabilitas mutasi
        elite_size: Jumlah elit yang dipertahankan
    
    Returns:
        Dictionary berisi hasil optimasi
    """
    
    n_cities = len(cities)
    
    # Fungsi hitung jarak rute
    def route_distance(route):
        total = 0
        for i in range(len(route)):
            total += distance_matrix[route[i]][route[(i+1) % len(route)]]
        return total
    
    # Buat individu acak
    def create_individual(n):
        ind = list(range(n))
        random.shuffle(ind)
        return ind
    
    # Inisialisasi populasi
    def initial_population(size, n):
        return [create_individual(n) for _ in range(size)]
    
    # Tournament selection
    def tournament_selection(pop, k):
        tournament = random.sample(pop, k)
        return min(tournament, key=lambda ind: route_distance(ind))
    
    # Ordered crossover (OX)
    def ordered_crossover(p1, p2):
        a, b = sorted(random.sample(range(len(p1)), 2))
        child = [-1] * len(p1)
        child[a:b+1] = p1[a:b+1]
        p2_idx = 0
        for i in range(len(p1)):
            if child[i] == -1:
                while p2[p2_idx] in child:
                    p2_idx += 1
                child[i] = p2[p2_idx]
        return child
    
    # Swap mutation
    def swap_mutation(ind):
        a, b = random.sample(range(len(ind)), 2)
        ind[a], ind[b] = ind[b], ind[a]
    
    # Inisialisasi populasi
    pop = initial_population(pop_size, n_cities)
    best = min(pop, key=lambda ind: route_distance(ind))
    best_dist = route_distance(best)
    
    evolution_log = []
    
    # Main GA loop
    for g in range(generations):
        new_pop = []
        
        # Sort populasi berdasarkan fitness
        pop = sorted(pop, key=lambda ind: route_distance(ind))
        
        # Update best solution
        if route_distance(pop[0]) < best_dist:
            best = pop[0][:]
            best_dist = route_distance(best)
        
        # Log setiap 10 generasi atau generasi pertama/terakhir
        if g == 0 or g == generations - 1 or (g + 1) % 10 == 0:
            best_route_names = [cities[i] for i in best]
            evolution_log.append({
                'generation': g + 1,
                'route': best_route_names,
                'distance': best_dist
            })
        
        # Elitism: pertahankan individu terbaik
        new_pop.extend([ind[:] for ind in pop[:elite_size]])
        
        # Reproduksi
        while len(new_pop) < pop_size:
            p1 = tournament_selection(pop, tournament_k)
            p2 = tournament_selection(pop, tournament_k)
            
            # Crossover
            if random.random() < crossover_rate:
                child = ordered_crossover(p1, p2)
            else:
                child = p1[:]
            
            # Mutasi
            if random.random() < mutation_rate:
                swap_mutation(child)
            
            new_pop.append(child)
        
        pop = new_pop[:pop_size]
    
    # Hasil akhir
    best_route = [cities[i] for i in best]
    
    return {
        'route': best_route,
        'distance': best_dist,
        'evolution_log': evolution_log
    }
print("\nHasil tersimpan di: hasil_TSP_GA.csv")