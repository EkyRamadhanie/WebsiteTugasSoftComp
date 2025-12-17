import numpy as np

# ----------------------------------------------------------------------
## 1. Fungsi Keanggotaan Generalized Bell-Shaped (gdbell_mf)
# Rumus: mu(x) = 1 / (1 + |(x - c) / a|^(2b))
# Parameter:
# x: Input variabel
# a: Lebar (width) kurva
# b: Kemiringan (slope) kurva
# c: Pusat (center) kurva
# ----------------------------------------------------------------------
def gdbell_mf(x, a, b, c):
    """
    Menghitung nilai keanggotaan (membership value) menggunakan 
    fungsi Generalized Bell-Shaped (gdbell).
    """
    # Menggunakan np.abs untuk nilai mutlak
    return 1 / (1 + np.abs((x - c) / a) ** (2 * b))

# ----------------------------------------------------------------------
## 2. Aturan Sugeno
# Rule 1: f1 = 0.1x + 0.1y + 0.1
# Rule 2: f2 = 10x + 10y + 10
# ----------------------------------------------------------------------
def def1(x, y):
    """
    Mengembalikan output Sugeno untuk Rule 1.
    """
    return 0.1 * x + 0.1 * y + 0.1

def def2(x, y):
    """
    Mengembalikan output Sugeno untuk Rule 2.
    """
    return 10 * x + 10 * y + 10

# ----------------------------------------------------------------------
## 3. Hitung ANFIS untuk input (x, y) dengan parameter dinamis
# ----------------------------------------------------------------------
def anfis(x, y, params_A1, params_B1, params_A2, params_B2):
    """
    Melakukan proses inferensi ANFIS berdasarkan input x dan y.
    Parameter gdbell untuk setiap membership function:
    - params_A1: [a, b, c] untuk A1(x)
    - params_B1: [a, b, c] untuk B1(y)
    - params_A2: [a, b, c] untuk A2(x)
    - params_B2: [a, b, c] untuk B2(y)
    """
    
    # Hitung nilai keanggotaan menggunakan fungsi gdbell
    A1 = gdbell_mf(x, params_A1[0], params_A1[1], params_A1[2])
    B1 = gdbell_mf(y, params_B1[0], params_B1[1], params_B1[2])
    A2 = gdbell_mf(x, params_A2[0], params_A2[1], params_A2[2])
    B2 = gdbell_mf(y, params_B2[0], params_B2[1], params_B2[2])

    # Layer 2 - Firing Strength (Kekuatan Pemicuan)
    # wi = AND(A(x), B(y)) -> dihitung sebagai perkalian
    w1 = A1 * B1
    w2 = A2 * B2

    # Layer 3 - Normalisasi Firing Strength
    w_sum = w1 + w2
    # Normalisasi: wi_norm = wi / sum(w)
    W1 = w1 / w_sum if w_sum != 0 else 0
    W2 = w2 / w_sum if w_sum != 0 else 0

    # Layer 4 - Weighted Output (Output Berbobot)
    # Output berbobot: out_i = wi_norm * fi(x, y)
    out1 = W1 * def1(x, y)
    out2 = W2 * def2(x, y)

    # Layer 5 - Output Total
    # Output total: output = sum(out_i)
    output = out1 + out2

    return {
        "A1": A1, "B1": B1, "A2": A2, "B2": B2,
        "w1": w1, "w2": w2,
        "W1": W1, "W2": W2,
        "out1": out1, "out2": out2,
        "final_output": output
    }

# ----------------------------------------------------------------------
## 4. Fungsi untuk user input dan proses
# ----------------------------------------------------------------------
def proses_anfis():
    """
    Fungsi untuk menerima input dari user dan memproses ANFIS.
    """
    print("\n======================================")
    print("   SISTEM ANFIS - INPUT DINAMIS")
    print("======================================\n")
    
    # Input nilai x dan y
    try:
        x = float(input("Masukkan nilai x: "))
        y = float(input("Masukkan nilai y: "))
        
        print("\n--- Parameter Membership Function A1(x) ---")
        a1_a = float(input("Masukkan parameter a untuk A1: "))
        a1_b = float(input("Masukkan parameter b untuk A1: "))
        a1_c = float(input("Masukkan parameter c untuk A1: "))
        
        print("\n--- Parameter Membership Function B1(y) ---")
        b1_a = float(input("Masukkan parameter a untuk B1: "))
        b1_b = float(input("Masukkan parameter b untuk B1: "))
        b1_c = float(input("Masukkan parameter c untuk B1: "))
        
        print("\n--- Parameter Membership Function A2(x) ---")
        a2_a = float(input("Masukkan parameter a untuk A2: "))
        a2_b = float(input("Masukkan parameter b untuk A2: "))
        a2_c = float(input("Masukkan parameter c untuk A2: "))
        
        print("\n--- Parameter Membership Function B2(y) ---")
        b2_a = float(input("Masukkan parameter a untuk B2: "))
        b2_b = float(input("Masukkan parameter b untuk B2: "))
        b2_c = float(input("Masukkan parameter c untuk B2: "))
        
        # Proses ANFIS
        result = anfis(
            x, y,
            [a1_a, a1_b, a1_c],
            [b1_a, b1_b, b1_c],
            [a2_a, a2_b, a2_c],
            [b2_a, b2_b, b2_c]
        )
        
        # Tampilkan hasil
        print(f"\n{'='*50}")
        print(f"   HASIL PERHITUNGAN ANFIS (x={x}, y={y})")
        print(f"{'='*50}")
        print(f"\nLayer 1 - Nilai Keanggotaan:")
        print(f"  A1(x) = {result['A1']:.6f}")
        print(f"  B1(y) = {result['B1']:.6f}")
        print(f"  A2(x) = {result['A2']:.6f}")
        print(f"  B2(y) = {result['B2']:.6f}")
        print(f"\nLayer 2 - Firing Strength:")
        print(f"  w1 = A1 * B1 = {result['w1']:.6f}")
        print(f"  w2 = A2 * B2 = {result['w2']:.6f}")
        print(f"\nLayer 3 - Normalized Firing Strength:")
        print(f"  W1 = {result['W1']:.6f}")
        print(f"  W2 = {result['W2']:.6f}")
        print(f"\nLayer 4 - Weighted Output:")
        print(f"  out1 = W1 * f1 = {result['out1']:.6f}")
        print(f"  out2 = W2 * f2 = {result['out2']:.6f}")
        print(f"\nLayer 5 - Output Akhir:")
        print(f"  OUTPUT FINAL = {result['final_output']:.6f}")
        print(f"{'='*50}\n")
        
    except ValueError:
        print("\n[ERROR] Input tidak valid! Harap masukkan angka.")
    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan: {e}")

# ----------------------------------------------------------------------
## 5. Main Program
# ----------------------------------------------------------------------
if __name__ == "__main__":
    while True:
        proses_anfis()
        
        # Tanya user apakah ingin menghitung lagi
        lagi = input("\nApakah Anda ingin menghitung lagi? (y/n): ").lower()
        if lagi != 'y':
            print("\nTerima kasih telah menggunakan sistem ANFIS!")
            break