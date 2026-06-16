from pathlib import Path
import polars as pl

HERE = Path(__file__).parent
PARQUET_FILE = HERE / 'dataset_completo.parquet'

def main() -> None:
    if not PARQUET_FILE.exists():
        raise FileNotFoundError(f'No se encontró el archivo: {PARQUET_FILE}')
    
    # Leer el archivo Parquet
    df = pl.read_parquet(PARQUET_FILE)
    
    print(f'═' * 80)
    print(f'INFORMACIÓN DEL ARCHIVO PARQUET')
    print(f'═' * 80)
    print(f'Archivo: {PARQUET_FILE.name}')
    print(f'Filas: {df.height:,}')
    print(f'Columnas: {df.width}')
    print()
    
    print(f'SCHEMA (tipos de datos):')
    print(f'─' * 80)
    for col, dtype in zip(df.columns, df.schema.values()):
        print(f'  {col:30} → {dtype}')
    print()
    
    print(f'PRIMERAS 10 FILAS:')
    print(f'─' * 80)
    print(df.head(10))
    print()
    
    print(f'ESTADÍSTICAS BÁSICAS (columnas numéricas):')
    print(f'─' * 80)
    print(df.describe())

if __name__ == '__main__':
    main()
