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
    # Jika tugas2.py, tugas3.py, atau tugas4.py, redirect ke form input
    if filename == 'tugas2.py':
        return render_template('form_tugas2.html')
    elif filename == 'tugas3.py':
        return render_template('form_tugas3.html')
    elif filename == 'tugas4.py':
        return render_template('form_tugas4.html')
    
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


@app.route('/run_tugas4', methods=['POST'])
def run_tugas4():
    try:
        # Ambil parameter dari form
        x = float(request.form.get('x', 3))
        y = float(request.form.get('y', 4))
        
        # Parameter A1
        a1_a = float(request.form.get('a1_a', 2))
        a1_b = float(request.form.get('a1_b', 2))
        a1_c = float(request.form.get('a1_c', 2))
        
        # Parameter B1
        b1_a = float(request.form.get('b1_a', 2))
        b1_b = float(request.form.get('b1_b', 2))
        b1_c = float(request.form.get('b1_c', 3))
        
        # Parameter A2
        a2_a = float(request.form.get('a2_a', 2))
        a2_b = float(request.form.get('a2_b', 2))
        a2_c = float(request.form.get('a2_c', 5))
        
        # Parameter B2
        b2_a = float(request.form.get('b2_a', 2))
        b2_b = float(request.form.get('b2_b', 2))
        b2_c = float(request.form.get('b2_c', 7))
        
        # Load dan jalankan ANFIS
        import importlib.util
        spec = importlib.util.spec_from_file_location("tugas4", os.path.join(app.root_path, 'hasil_tugas', 'tugas4.py'))
        tugas4_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tugas4_module)
        
        result = tugas4_module.anfis(
            x, y,
            [a1_a, a1_b, a1_c],
            [b1_a, b1_b, b1_c],
            [a2_a, a2_b, a2_c],
            [b2_a, b2_b, b2_c]
        )
        
        # Format output
        output = "=" * 70 + "\n"
        output += "     ADAPTIVE NEURO-FUZZY INFERENCE SYSTEM (ANFIS)\n"
        output += "=" * 70 + "\n\n"
        
        output += "INPUT VALUES:\n"
        output += f"- x = {x}\n"
        output += f"- y = {y}\n\n"
        
        output += "MEMBERSHIP FUNCTION PARAMETERS (Generalized Bell):\n"
        output += "-" * 70 + "\n"
        output += f"A1(x): a={a1_a}, b={a1_b}, c={a1_c}\n"
        output += f"B1(y): a={b1_a}, b={b1_b}, c={b1_c}\n"
        output += f"A2(x): a={a2_a}, b={a2_b}, c={a2_c}\n"
        output += f"B2(y): a={b2_a}, b={b2_b}, c={b2_c}\n"
        output += "-" * 70 + "\n\n"
        
        output += "FUZZY RULES (Sugeno):\n"
        output += "-" * 70 + "\n"
        output += "Rule 1: IF x is A1 AND y is B1 THEN f1 = 0.1x + 0.1y + 0.1\n"
        output += "Rule 2: IF x is A2 AND y is B2 THEN f2 = 10x + 10y + 10\n"
        output += "-" * 70 + "\n\n"
        
        output += "LAYER-BY-LAYER COMPUTATION:\n"
        output += "=" * 70 + "\n\n"
        
        output += "Layer 1 - Fuzzification (Membership Values):\n"
        output += "-" * 70 + "\n"
        output += f"  A1({x}) = {result['A1']:.6f}\n"
        output += f"  B1({y}) = {result['B1']:.6f}\n"
        output += f"  A2({x}) = {result['A2']:.6f}\n"
        output += f"  B2({y}) = {result['B2']:.6f}\n"
        output += "-" * 70 + "\n\n"
        
        output += "Layer 2 - Rule Activation (Firing Strength):\n"
        output += "-" * 70 + "\n"
        output += f"  w1 = A1 × B1 = {result['A1']:.6f} × {result['B1']:.6f} = {result['w1']:.6f}\n"
        output += f"  w2 = A2 × B2 = {result['A2']:.6f} × {result['B2']:.6f} = {result['w2']:.6f}\n"
        output += "-" * 70 + "\n\n"
        
        output += "Layer 3 - Normalization:\n"
        output += "-" * 70 + "\n"
        w_sum = result['w1'] + result['w2']
        output += f"  Sum(w) = w1 + w2 = {w_sum:.6f}\n"
        output += f"  W1 = w1/Sum(w) = {result['w1']:.6f}/{w_sum:.6f} = {result['W1']:.6f}\n"
        output += f"  W2 = w2/Sum(w) = {result['w2']:.6f}/{w_sum:.6f} = {result['W2']:.6f}\n"
        output += "-" * 70 + "\n\n"
        
        f1_val = 0.1 * x + 0.1 * y + 0.1
        f2_val = 10 * x + 10 * y + 10
        
        output += "Layer 4 - Defuzzification (Weighted Output):\n"
        output += "-" * 70 + "\n"
        output += f"  f1 = 0.1×{x} + 0.1×{y} + 0.1 = {f1_val:.6f}\n"
        output += f"  f2 = 10×{x} + 10×{y} + 10 = {f2_val:.6f}\n\n"
        output += f"  out1 = W1 × f1 = {result['W1']:.6f} × {f1_val:.6f} = {result['out1']:.6f}\n"
        output += f"  out2 = W2 × f2 = {result['W2']:.6f} × {f2_val:.6f} = {result['out2']:.6f}\n"
        output += "-" * 70 + "\n\n"
        
        output += "Layer 5 - Final Output:\n"
        output += "=" * 70 + "\n"
        output += f"  OUTPUT = out1 + out2\n"
        output += f"         = {result['out1']:.6f} + {result['out2']:.6f}\n"
        output += f"         = {result['final_output']:.6f}\n"
        output += "=" * 70 + "\n"
        
        return render_template('hasil.html', filename='tugas4.py', result=output)
    
    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        return render_template('hasil.html', filename='tugas4.py', result=error_msg)


if __name__ == '__main__':
    app.run(debug=True)
