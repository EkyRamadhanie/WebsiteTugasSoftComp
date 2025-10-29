# -*- coding: utf-8 -*-
# ===============================================
# Tugas 1 - Algoritma Kecerdasan Buatan
# Penulis: Eky Ramadhanie
# ===============================================

def main():
    print("===== TUGAS 1 - PERBANDINGAN ALGORITMA AI =====\n")
    
    # -------------------------------
    # 1. Algoritma Fuzzy Logic
    # -------------------------------
    print("1. Algoritma Fuzzy Logic")
    print("""
Pengertian:
Fuzzy Logic (Logika Fuzzy) adalah metode komputasi yang meniru cara manusia mengambil keputusan
berdasarkan ketidakpastian dan nilai kebenaran yang bersifat derajat (0 sampai 1), bukan absolut.

Kelebihan:
- Mampu menangani data yang samar atau tidak pasti.
- Mudah diimplementasikan untuk sistem kontrol (misalnya suhu, kecepatan, kecerahan).
- Dapat menggabungkan pengalaman manusia ke dalam sistem berbasis aturan (IF–THEN).

Kekurangan:
- Sulit menentukan fungsi keanggotaan yang optimal.
- Hasil keputusan bisa subjektif tergantung rancangan aturan.
- Tidak cocok untuk sistem yang butuh akurasi numerik tinggi.
""")

    # -------------------------------
    # 2. Algoritma Jaringan Saraf Tiruan (JST)
    # -------------------------------
    print("2. Algoritma Jaringan Saraf Tiruan (Neural Network)")
    print("""
Pengertian:
Jaringan Saraf Tiruan (JST) adalah model komputasi yang terinspirasi dari cara kerja otak manusia,
terdiri atas neuron-neuron buatan yang saling terhubung dan belajar dari data melalui proses training.

Kelebihan:
- Mampu mempelajari pola kompleks dari data besar.
- Cocok untuk klasifikasi, prediksi, pengenalan pola, dan pengolahan citra.
- Dapat memperbaiki akurasi seiring banyaknya data pelatihan.

Kekurangan:
- Membutuhkan data besar dan waktu pelatihan yang lama.
- Hasil sulit dijelaskan (black box).
- Konsumsi sumber daya komputasi tinggi.
""")

    # -------------------------------
    # 3. Algoritma Genetika
    # -------------------------------
    print("3. Algoritma Genetika (Genetic Algorithm)")
    print("""
Pengertian:
Algoritma Genetika adalah algoritma optimasi berbasis prinsip evolusi biologis — seleksi alam, crossover,
dan mutasi — untuk mencari solusi terbaik dari suatu permasalahan kompleks.

Kelebihan:
- Efektif mencari solusi global pada masalah kompleks.
- Tidak memerlukan turunan matematis atau gradien.
- Mampu bekerja pada fungsi non-linear dan multi-objektif.

Kekurangan:
- Prosesnya acak, jadi hasil bisa berbeda tiap eksekusi.
- Membutuhkan parameter (populasi, mutasi, crossover) yang tepat.
- Tidak efisien untuk masalah sederhana dengan solusi langsung.
""")

    print("===============================================\n")
    print("Tugas 1 selesai ditampilkan.")


if __name__ == "__main__":
    main()
