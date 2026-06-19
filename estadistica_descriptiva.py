import polars as pl
import time
import matplotlib.pyplot as plt

# =========================
# TIMER
# =========================
inicio = time.perf_counter()

# =========================
# CARGA PARQUET
# =========================
df = pl.read_parquet("dataset_completo.parquet")

df_sel = df.select(["ENTIDAD_UM", "ENTIDAD_RES"])

total = df_sel.height

# =========================
# FUNCIÓN PARA ESTADÍSTICA
# =========================
def analisis_categoria(columna):
    freq = (
        df_sel
        .group_by(columna)
        .agg(pl.len().alias("frecuencia"))
        .sort("frecuencia", descending=True)
    )

    freq = freq.with_columns(
        (pl.col("frecuencia") / total * 100).alias("porcentaje")
    )

    moda = freq.row(0)[0]  # valor más frecuente

    return freq, moda

# =========================
# ENTIDAD_UM
# =========================
freq_um, moda_um = analisis_categoria("ENTIDAD_UM")

# =========================
# ENTIDAD_RES
# =========================
freq_res, moda_res = analisis_categoria("ENTIDAD_RES")

# =========================
# RESUMEN GENERAL
# =========================
resumen = df_sel.select([
    pl.col("ENTIDAD_UM").n_unique().alias("unicas_UM"),
    pl.col("ENTIDAD_RES").n_unique().alias("unicas_RES"),
    pl.len().alias("total_registros")
])

# =========================
# TIEMPO
# =========================
fin = time.perf_counter()
tiempo = fin - inicio

# =========================
# GUARDAR TXT
# =========================
with open("Estadistica_descriptiva/reporte_estadistico2.txt", "w", encoding="utf-8") as f:
    f.write("REPORTE ESTADÍSTICO COVID MÉXICO\n\n")

    f.write("=== RESUMEN GENERAL ===\n")
    f.write(str(resumen) + "\n\n")

    f.write("=== ENTIDAD_UM ===\n")
    f.write(str(freq_um) + "\n\n")
    f.write(f"MODA ENTIDAD_UM: {moda_um}\n\n")

    f.write("=== ENTIDAD_RES ===\n")
    f.write(str(freq_res) + "\n\n")
    f.write(f"MODA ENTIDAD_RES: {moda_res}\n\n")

    f.write(f"TIEMPO DE EJECUCIÓN: {tiempo:.4f} segundos\n")



print(f"Listo en {tiempo:.4f} segundos")
print("Reporte: reporte_estadistico.txt")
