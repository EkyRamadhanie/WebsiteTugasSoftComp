from flask import Flask, render_template, url_for
import os, subprocess

app = Flask(__name__)

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
    file_path = os.path.join(app.root_path, 'hasil_tugas', filename)
    try:
        result = subprocess.check_output(['python', file_path], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        result = e.output

    return render_template('hasil.html', filename=filename, result=result)


if __name__ == '__main__':
    app.run(debug=True)
