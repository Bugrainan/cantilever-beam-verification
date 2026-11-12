import matplotlib.pyplot as plt


def calculate_analytical_beam(b, h, length, force, E):
    """Euler-Bernoulli ankastre kiriş teorik hesaplamaları (mm, N, MPa)."""
    moment_of_inertia = (b * (h**3)) / 12.0
    max_moment = force * length
    max_stress = (max_moment * (h / 2.0)) / moment_of_inertia
    max_deflection = (force * (length**3)) / (3.0 * E * moment_of_inertia)
    return max_deflection, max_stress


def main():
    # Geometri, yük ve malzeme parametreleri (Structural Steel)
    b, h, length = 100.0, 200.0, 2000.0  # mm
    force = 10000.0  # N (10 kN)
    E = 200000.0  # MPa (200 GPa)

    theo_defl, theo_stress = calculate_analytical_beam(b, h, length, force, E)

    # ANSYS Workbench 2026 R1 Mesh Convergence verileri
    mesh_sizes = [50, 25, 15]  # mm
    ansys_defl = [2.0105, 2.0117, 2.0122]  # mm
    ansys_stress = [31.061, 35.996, 43.736]  # MPa

    print(f"Teorik Maksimum Sehim   : {theo_defl:.4f} mm")
    print(f"Teorik Maksimum Gerilme : {theo_stress:.4f} MPa\n")
    print(f"{'Mesh (mm)':<10} | {'Sehim (mm)':<12} | {'Fark (%)':<10} | {'Gerilme (MPa)':<14} | {'Fark (%)':<10}")
    print("-" * 68)

    for size, d, s in zip(mesh_sizes, ansys_defl, ansys_stress):
        d_err = abs(d - theo_defl) / theo_defl * 100.0
        s_err = abs(s - theo_stress) / theo_stress * 100.0
        print(f"{size:<10} | {d:<12.4f} | {d_err:<10.2f} | {s:<14.3f} | {s_err:<10.2f}")

    # Yakınsama Grafiği Oluşturma
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    ax1.plot(mesh_sizes, ansys_defl, "o-", color="#1f77b4", linewidth=2, label="ANSYS 3D FEA")
    ax1.axhline(theo_defl, color="#d62728", linestyle="--", label="Euler-Bernoulli (2.000 mm)")
    ax1.set_title("Deformasyon Yakınsaması (Mesh Convergence)")
    ax1.set_xlabel("Eleman Boyutu (mm)")
    ax1.set_ylabel("Maksimum Sehim (mm)")
    ax1.set_ylim(1.98, 2.03)
    ax1.invert_xaxis()
    ax1.grid(True, linestyle=":", alpha=0.7)
    ax1.legend()

    ax2.plot(mesh_sizes, ansys_stress, "s-", color="#ff7f0e", linewidth=2, label="ANSYS Kök Gerilmesi")
    ax2.axhline(theo_stress, color="#2ca02c", linestyle="--", label="Euler-Bernoulli (30.000 MPa)")
    ax2.set_title("Ankastre Köşede Gerilme Tekilliği")
    ax2.set_xlabel("Eleman Boyutu (mm)")
    ax2.set_ylabel("Maks. Equivalent Stress (MPa)")
    ax2.invert_xaxis()
    ax2.grid(True, linestyle=":", alpha=0.7)
    ax2.legend()

    plt.tight_layout()
    plt.savefig("images/mesh_convergence.png", dpi=300)
    print("\nGrafik 'images/mesh_convergence.png' olarak kaydedildi.")


if __name__ == "__main__":
    main()
