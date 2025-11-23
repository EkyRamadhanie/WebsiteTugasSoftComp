import random

def knapsack_ga(items, capacity, pop_size, generations, crossover_rate=0.8, mutation_rate=0.1, elitism=True):
    """
    Algoritma Genetika untuk Knapsack Problem
    dengan Roulette Selection dan Elitism
    """
    item_list = list(items.keys())
    n_items = len(item_list)
    
    # Fungsi decode: mengubah kromosom menjadi item, berat, nilai
    def decode(chromosome):
        total_weight = 0
        total_value = 0
        chosen_items = []
        for gene, name in zip(chromosome, item_list):
            if gene == 1:
                total_weight += items[name]['weight']
                total_value += items[name]['value']
                chosen_items.append(name)
        return chosen_items, total_weight, total_value
    
    # Fungsi fitness dengan penalti
    def fitness(chromosome):
        _, total_weight, total_value = decode(chromosome)
        if total_weight <= capacity:
            return total_value
        else:
            return 0  # Penalti untuk berat berlebih
    
    # Roulette Wheel Selection
    def roulette_selection(population, fitnesses):
        total_fit = sum(fitnesses)
        if total_fit == 0:
            return random.choice(population)
        
        pick = random.uniform(0, total_fit)
        current = 0
        for chrom, fit in zip(population, fitnesses):
            current += fit
            if current >= pick:
                return chrom
        return population[-1]  # fallback
    
    # Single-point crossover
    def crossover(p1, p2):
        point = random.randint(1, len(p1) - 1)
        child1 = p1[:point] + p2[point:]
        child2 = p2[:point] + p1[point:]
        return child1, child2
    
    # Mutasi bit flip
    def mutate(chromosome, rate):
        return [1 - g if random.random() < rate else g for g in chromosome]
    
    # Inisialisasi populasi acak
    population = [[random.randint(0, 1) for _ in range(n_items)] for _ in range(pop_size)]
    
    # Simpan log evolusi
    evolution_log = []
    
    # Proses evolusi
    for gen in range(generations):
        # Hitung fitness semua individu
        fitnesses = [fitness(ch) for ch in population]
        
        # Cari individu terbaik
        best_index = fitnesses.index(max(fitnesses))
        best_chrom = population[best_index]
        best_fit = fitnesses[best_index]
        best_items, w, v = decode(best_chrom)
        
        # Simpan log generasi ini
        evolution_log.append({
            'generation': gen + 1,
            'chromosome': best_chrom.copy(),
            'items': best_items.copy(),
            'weight': w,
            'value': v,
            'fitness': best_fit
        })
        
        # Buat populasi baru
        new_population = []
        
        # Elitism: pertahankan individu terbaik
        if elitism:
            new_population.append(best_chrom)
        
        # Reproduksi hingga populasi penuh
        while len(new_population) < pop_size:
            # Seleksi orang tua dengan roulette wheel
            parent1 = roulette_selection(population, fitnesses)
            parent2 = roulette_selection(population, fitnesses)
            
            # Crossover
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]
            
            # Mutasi
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            
            # Tambahkan ke populasi baru
            new_population.extend([child1, child2])
        
        # Batasi ukuran populasi
        population = new_population[:pop_size]
    
    # Hasil akhir
    fitnesses = [fitness(ch) for ch in population]
    best_index = fitnesses.index(max(fitnesses))
    best_chrom = population[best_index]
    best_items, w, v = decode(best_chrom)
    best_fit = fitnesses[best_index]
    
    return {
        "chromosome": best_chrom,
        "items": best_items,
        "weight": w,
        "value": v,
        "fitness": best_fit,
        "evolution_log": evolution_log
    }
