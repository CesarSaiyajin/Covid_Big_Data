from pathlib import Path
import polars as pl
import time
import os
from datetime import datetime

HERE = Path(__file__).parent
CSV_FILE = HERE / 'dataset_completo.csv'
PARQUET_FILE = HERE / 'dataset_completo.parquet'

def main() -> None:
    inicio = time.time()
    
    if not CSV_FILE.exists():
        raise FileNotFoundError(f'No se encontró el archivo: {CSV_FILE}')
    
    print(f'Leyendo CSV: {CSV_FILE}')
    df = pl.read_csv(
        CSV_FILE,
        encoding='utf-8',
        infer_schema_length=10000,
        truncate_ragged_lines=False,
        ignore_errors=False,
    )
    print(f'Datos leídos: {df.height:,} filas x {df.width} columnas')
    
    print(f'Convirtiendo a Parquet...')
    df.write_parquet(PARQUET_FILE, compression='snappy')
    
    parquet_size = PARQUET_FILE.stat().st_size / (1024 * 1024)  # MB
    csv_size = CSV_FILE.stat().st_size / (1024 * 1024)  # MB
    
    print(f'✓ Archivo Parquet creado: {PARQUET_FILE}')
    print(f'  Tamaño CSV:     {csv_size:.2f} MB')
    print(f'  Tamaño Parquet: {parquet_size:.2f} MB')
    print(f'  Compresión:     {(1 - parquet_size/csv_size)*100:.1f}%')
    
    # Guardar el tiempo de ejecución
    duracion = time.time() - inicio
    
    if not os.path.exists("Tiempos"):
        os.makedirs("Tiempos")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_tiempo = os.path.join("Tiempos", f"tiempo_ejecucion_convertir_a_parquet_{timestamp}.txt")
    
    with open(archivo_tiempo, "w") as f:
        f.write(f"Tiempo de ejecución de convertir_a_parquet.py\n")
        f.write(f"===========================================\n")
        f.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duración: {duracion:.2f} segundos\n")
        f.write(f"Filas procesadas: {df.height:,}\n")
        f.write(f"Tamaño CSV: {csv_size:.2f} MB\n")
        f.write(f"Tamaño Parquet: {parquet_size:.2f} MB\n")
    
    print(f"Tiempo de ejecución guardado en: {archivo_tiempo}")

if __name__ == '__main__':
    main()
