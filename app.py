from flask import Flask, render_template, url_for, request
import os, subprocess, sys, random

app = Flask(__name__)

# Tambahkan folder hasil_tugas ke sys.path agar bisa import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hasil_tugas'))

# Import fungsi knapsack_ga dari tugas2
def load_knapsack_ga():
    """Load fungsi knapsack_ga dari tugas2.py"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("tugas2", os.path.join(app.root_path, 'hasil_tugas', 'tugas2.py'))
    tugas2_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tugas2_module)
    return tugas2_module.knapsack_ga

@app.route('/')
def index():
    folder = os.path.join(app.root_path, 'hasil_tugas')
    tugas_list = []
    for f in os.listdir(folder):
        if f.endswith('.py'):
            # ambil nama tanpa .py dan ubah jadi format "TUGAS X"
            nama_tugas = f.replace('.py', '').replace('tugas', 'TUGAS ').upper()
            tugas_list.append((f, nama_tugas))
    return render_template('index.html', tugas_list=tugas_list)


@app.route('/run/<filename>')
def run_python(filename):
    # Jika tugas2.py atau tugas3.py, redirect ke form input
    if filename == 'tugas2.py':
        return render_template('form_tugas2.html')
    elif filename == 'tugas3.py':
        return render_template('form_tugas3.html')
    
    file_path = os.path.join(app.root_path, 'hasil_tugas', filename)
    try:
        result = subprocess.check_output(['python', file_path], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        result = e.output

    return render_template('hasil.html', filename=filename, result=result)


@app.route('/run_tugas2', methods=['POST'])
def run_tugas2():
    try:
        # Ambil data dari form
        capacity = int(request.form.get('capacity', 15))
        population = int(request.form.get('population', 8))
        generation = int(request.form.get('generation', 10))
        crossover_rate = float(request.form.get('crossover_rate', 0.8))
        mutation_rate = float(request.form.get('mutation_rate', 0.1))
        
        # Parse items dari form (format: nama,berat,nilai per baris)
        items_text = request.form.get('items', '')
        items = {}
        
        if items_text.strip():
            for line in items_text.strip().split('\n'):
                parts = line.split(',')
                if len(parts) == 3:
                    name = parts[0].strip()
                    weight = int(parts[1].strip())
                    value = int(parts[2].strip())
                    items[name] = {"weight": weight, "value": value}
        
        # Jika tidak ada items, gunakan default (A, B, C, D)
        if not items:
            items = {
                "A": {"weight": 7, "value": 5},
                "B": {"weight": 2, "value": 4},
                "C": {"weight": 1, "value": 7},
                "D": {"weight": 9, "value": 2}
            }
        
        # Jalankan algoritma GA
        knapsack_ga = load_knapsack_ga()
        result = knapsack_ga(items, capacity, population, generation, crossover_rate, mutation_rate)
        
        # Format output dengan detail evolusi
        output = "=" * 65 + "\n"
        output += "     GENETIC ALGORITHM - KNAPSACK PROBLEM\n"
        output += "=" * 65 + "\n\n"
        
        output += "PARAMETER ALGORITMA:\n"
        output += f"- Kapasitas Tas        : {capacity} kg\n"
        output += f"- Ukuran Populasi      : {population}\n"
        output += f"- Jumlah Generasi      : {generation}\n"
        output += f"- Crossover Rate       : {crossover_rate}\n"
        output += f"- Mutation Rate        : {mutation_rate}\n"
        output += f"- Elitism              : Aktif\n\n"
        
        output += "BARANG YANG TERSEDIA:\n"
        output += "-" * 65 + "\n"
        for name, data in items.items():
            output += f"  {name:10s} | Berat: {data['weight']:2d} kg | Nilai: ${data['value']:3d}\n"
        output += "-" * 65 + "\n\n"
        
        output += "PROSES EVOLUSI (PER GENERASI):\n"
        output += "-" * 65 + "\n"
        
        # Tampilkan evolusi per generasi
        for log in result['evolution_log']:
            output += f"Generasi {log['generation']:2d}: "
            output += f"Kromosom={log['chromosome']} | "
            output += f"Item=[{', '.join(log['items']) if log['items'] else 'kosong'}] | "
            output += f"Berat={log['weight']:2d} | "
            output += f"Nilai=${log['value']:3d}\n"
        
        output += "-" * 65 + "\n\n"
        
        output += "=" * 65 + "\n"
        output += "                       HASIL AKHIR\n"
        output += "=" * 65 + "\n"
        output += f"Kromosom Terbaik   : {result['chromosome']}\n"
        output += f"Item Terpilih      : [{', '.join(result['items']) if result['items'] else 'kosong'}]\n"
        output += f"Total Berat        : {result['weight']} kg (dari {capacity} kg)\n"
        output += f"Total Nilai        : ${result['value']}\n"
        output += f"Fitness Akhir      : {result['fitness']}\n"
        output += "=" * 65 + "\n"
        
        return render_template('hasil.html', filename='tugas2.py', result=output)
    
    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        return render_template('hasil.html', filename='tugas2.py', result=error_msg)


@app.route('/run_tugas3', methods=['POST'])
def run_tugas3():
    try:
        # Ambil parameter dari form
        pop_size = int(request.form.get('pop_size', 50))
        generations = int(request.form.get('generations', 100))
        tournament_k = int(request.form.get('tournament_k', 5))
        crossover_rate = float(request.form.get('crossover_rate', 0.9))
        mutation_rate = float(request.form.get('mutation_rate', 0.2))
        elite_size = int(request.form.get('elite_size', 1))
        
        # Parse distance matrix dari form
        cities_input = request.form.get('cities', '').strip()
        matrix_input = request.form.get('matrix', '').strip()
        
        # Default data (contoh 5 kota)
        if not cities_input or not matrix_input:
            cities = ['Jakarta', 'Bandung', 'Surabaya', 'Yogyakarta', 'Semarang']
            distance_matrix = [
                [0, 150, 780, 500, 450],
                [150, 0, 730, 380, 400],
                [780, 730, 0, 320, 410],
                [500, 380, 320, 0, 120],
                [450, 400, 410, 120, 0]
            ]
        else:
            # Parse cities
            cities = [c.strip() for c in cities_input.split(',')]
            
            # Parse distance matrix
            distance_matrix = []
            for line in matrix_input.strip().split('\n'):
                row = [float(x.strip()) for x in line.split(',')]
                distance_matrix.append(row)
        
        # Load dan jalankan TSP GA
        import importlib.util
        spec = importlib.util.spec_from_file_location("tugas3", os.path.join(app.root_path, 'hasil_tugas', 'tugas3.py'))
        tugas3_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tugas3_module)
        
        result = tugas3_module.tsp_genetic_algorithm(
            cities, distance_matrix, pop_size, generations,
            tournament_k, crossover_rate, mutation_rate, elite_size
        )
        
        # Format output
        output = "=" * 70 + "\n"
        output += "     TRAVELLING SALESMAN PROBLEM - GENETIC ALGORITHM\n"
        output += "=" * 70 + "\n\n"
        
        output += "PARAMETER ALGORITMA:\n"
        output += f"- Ukuran Populasi      : {pop_size}\n"
        output += f"- Jumlah Generasi      : {generations}\n"
        output += f"- Tournament Size (K)  : {tournament_k}\n"
        output += f"- Crossover Rate       : {crossover_rate}\n"
        output += f"- Mutation Rate        : {mutation_rate}\n"
        output += f"- Elite Size           : {elite_size}\n\n"
        
        output += "KOTA-KOTA:\n"
        output += "-" * 70 + "\n"
        for i, city in enumerate(cities):
            output += f"  {i}. {city}\n"
        output += "-" * 70 + "\n\n"
        
        output += "MATRIX JARAK:\n"
        output += "-" * 70 + "\n"
        # Header
        output += f"{'':12s}"
        for city in cities:
            output += f"{city[:10]:>12s}"
        output += "\n"
        # Rows
        for i, city in enumerate(cities):
            output += f"{city[:10]:12s}"
            for j in range(len(cities)):
                output += f"{distance_matrix[i][j]:>12.1f}"
            output += "\n"
        output += "-" * 70 + "\n\n"
        
        output += "PROSES EVOLUSI:\n"
        output += "-" * 70 + "\n"
        for log in result['evolution_log']:
            route_str = ' -> '.join(log['route'])
            output += f"Gen {log['generation']:3d}: {route_str} -> {log['route'][0]}\n"
            output += f"         Jarak: {log['distance']:.2f} km\n\n"
        output += "-" * 70 + "\n\n"
        
        output += "=" * 70 + "\n"
        output += "                       HASIL AKHIR\n"
        output += "=" * 70 + "\n"
        route_str = ' -> '.join(result['route']) + ' -> ' + result['route'][0]
        output += f"Rute Terbaik:\n  {route_str}\n\n"
        output += f"Total Jarak: {result['distance']:.2f} km\n"
        output += "=" * 70 + "\n"
        
        return render_template('hasil.html', filename='tugas3.py', result=output)
    
    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        return render_template('hasil.html', filename='tugas3.py', result=error_msg)


if __name__ == '__main__':
    app.run(debug=True)
