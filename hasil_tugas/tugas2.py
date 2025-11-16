import random

# 1. Data Masalah Knapsack
# -----------------------------
items = {
    'A': {'weight': 7, 'value': 5},
    'B': {'weight': 2, 'value': 4},
    'C': {'weight': 1, 'value': 7},
    'D': {'weight': 9, 'value': 2},
}

capacity = 15
item_list = list(items.keys())
n_items = len(item_list)

# 2. Fungsi bantu
# -----------------------------
def decode(chromosome):
    """Kembalikan list item, total berat, total nilai"""
    total_weight = 0
    total_value = 0
    chosen_items = []
    for gene, name in zip(chromosome, item_list):
        if gene == 1:
            total_weight += items[name]['weight']
            total_value += items[name]['value']
            chosen_items.append(name)
    return chosen_items, total_weight, total_value

def fitness(chromosome):
    """Fungsi fitness dengan penalti berat"""
    _, total_weight, total_value = decode(chromosome)
    if total_weight <= capacity:
        return total_value
    else:
        # Penalti berat berlebih (bisa diganti dengan 0 atau pengurangan)
        return 0

def roulette_selection(population, fitnesses):
    """Seleksi roulette wheel"""
    total_fit = sum(fitnesses)
    
    # Jika fitness nol, pilih acak
    if total_fit == 0:
        return random.choice(population)
    
    pick = random.uniform(0, total_fit)
    current = 0
    for chrom, fit in zip(population, fitnesses):
        current += fit
        if current >= pick:
            return chrom

def crossover(p1, p2):
    """Single-point crossover"""
    if len(p1) != len(p2):
        raise ValueError("Parent length mismatch")

    point = random.randint(1, len(p1) - 1)
    child1 = p1[:point] + p2[point:]
    child2 = p2[:point] + p1[point:]
    return child1, child2

def mutate(chromosome, mutation_rate=0.1):
    """Flip bit dengan probabilitas mutation_rate"""
    return [1 - g if random.random() < mutation_rate else g for g in chromosome]

# 3. Algoritma Genetika Utama
# -----------------------------
def genetic_algorithm(pop_size=10, generations=10, crossover_rate=0.8, mutation_rate=0.1, elitism=True):
    # Inisialisasi populasi acak
    population = [[random.randint(0, 1) for _ in range(n_items)] for _ in range(pop_size)]

    for gen in range(generations):
        # Hitung fitness
        fitnesses = [fitness(ch) for ch in population]

        # Catat individu terbaik
        best_index = fitnesses.index(max(fitnesses))
        best_chrom = population[best_index]
        best_fit = fitnesses[best_index]
        best_items, w, v = decode(best_chrom)

        print(f'Generasi {gen+1}:')
        print(f'Terbaik: {best_chrom} | Item: {best_items} | Berat: {w} | Nilai: {v} | Fitness: {best_fit}')
        print("-" * 65)

        # Buat generasi baru
        new_population = []

        # Elitism: pertahankan individu terbaik
        if elitism:
            new_population.append(best_chrom)

        # Reproduksi
        while len(new_population) < pop_size:
            # Seleksi orang tua
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

            # Tambah ke populasi baru
            new_population.extend([child1, child2])

        # Batasi ukuran populasi
        population = new_population[:pop_size]

    # Ambil hasil akhir
    fitnesses = [fitness(ch) for ch in population]
    best_index = fitnesses.index(max(fitnesses))
    best_chrom = population[best_index]
    best_items, w, v = decode(best_chrom)
    best_fit = fitnesses[best_index]

    print(f"\n{'=' * 20} HASIL AKHIR {'=' * 20}")
    print(f'Kromosom terbaik: {best_chrom}')
    print(f'Item terpilih: {best_items}')
    print(f'Total berat: {w} kg')
    print(f'Total nilai: ${v}')
    print(f'Fitness akhir: {best_fit}')
    print('=' * 50)


# 4. Jalankan Program
# -----------------------------
if __name__ == '__main__':
    random.seed(25)  # agar hasil replikasi konsisten
    genetic_algorithm(pop_size=8, generations=8, crossover_rate=0.8, mutation_rate=0.1)