from flask import Flask, render_template, url_for
import os
import subprocess

app = Flask(__name__)

# Folder tempat file Python disimpan
HASIL_TUGAS_DIR = os.path.join(app.root_path, "hasil_tugas")

@app.route("/")
def index():
    files = [f for f in os.listdir(HASIL_TUGAS_DIR) if f.endswith(".py")]
    return render_template("index.html", files=files)

@app.route("/run/<filename>")
def run_python(filename):
    file_path = os.path.join(HASIL_TUGAS_DIR, filename)
    if os.path.exists(file_path):
        # Jalankan file python dan ambil outputnya
        result = subprocess.run(["python3", file_path], capture_output=True, text=True)
        output = result.stdout + result.stderr
        return f"""
        <html>
            <head>
                <link rel='stylesheet' href='{url_for('static', filename='style.css')}'>
                <title>Output - {filename}</title>
            </head>
            <body>
                <div class='terminal'>
                    <h2>🐍 Output dari {filename}</h2>
                    <pre>{output}</pre>
                    <a href='/' class='btn'>⬅️ Kembali</a>
                </div>
            </body>
        </html>
        """
    else:
        return f"❌ File {filename} tidak ditemukan."


if __name__ == "__main__":
    app.run(debug=True)
