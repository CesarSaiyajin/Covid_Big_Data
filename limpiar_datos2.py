import csv
import time
import os
from datetime import datetime
from pathlib import Path

import polars as pl

HERE = Path(__file__).parent
SOURCE = HERE / 'primerlimpieza.csv'
CLEANED_RAW = HERE / 'primer_limpieza_temp.csv'
OUTPUT = HERE / 'segunda_limpieza.csv'
DELETED_OUTPUT = HERE / 'datos_eliminados.csv'

DATE_COLUMNS = [
    'FECHA_ACTUALIZACION',
    'FECHA_INGRESO',
    'FECHA_SINTOMAS',
    'FECHA_DEF',
]

SENTINEL_STRINGS = {'97', '99', '9999-99-99'}


def clean_raw_csv(source: Path, target: Path, deleted_file: Path) -> tuple[int, int]:
    if target.exists() and deleted_file.exists():
        print(f'Archivo limpio intermedio ya existe: {target}')
        return 0, 0

    with source.open('r', encoding='utf-8', newline='') as source_file, \
         target.open('w', encoding='utf-8', newline='') as target_file, \
         deleted_file.open('w', encoding='utf-8', newline='') as deleted_file_obj:
        
        reader = csv.reader(source_file)
        writer = csv.writer(target_file)
        deleted_writer = csv.writer(deleted_file_obj)

        header = next(reader)
        writer.writerow(header)
        
        # Agregar columna de razón de eliminación
        deleted_header = header + ['RAZON_ELIMINACION', 'NUMERO_FILA']
        deleted_writer.writerow(deleted_header)
        
        expected_columns = len(header)

        valid_rows = 0
        bad_rows = 0
        row_number = 1
        
        for row in reader:
            row_number += 1
            if len(row) != expected_columns:
                bad_rows += 1
                razon = f'Número incorrecto de columnas (esperado {expected_columns}, obtuvo {len(row)})'
                deleted_writer.writerow(row + [razon, row_number])
                continue
            writer.writerow(row)
            valid_rows += 1

            if valid_rows % 500_000 == 0:
                print(f'  Procesadas {valid_rows:,} filas válidas, {bad_rows:,} filas malas descartadas')

    print(f'Archivo intermedio creado: {target} (válidas={valid_rows:,}, descartadas={bad_rows:,})')
    print(f'Archivo de datos eliminados creado: {deleted_file}')
    return valid_rows, bad_rows


def normalize_sentinels(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        [
            pl.when(pl.col(c).cast(pl.Utf8).is_in(SENTINEL_STRINGS))
            .then(None)
            .otherwise(pl.col(c))
            .alias(c)
            for c in df.columns
        ]
    )


def parse_date_columns(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        [
            pl.when(pl.col(c).cast(pl.Utf8).is_in(SENTINEL_STRINGS))
            .then(None)
            .otherwise(pl.col(c).cast(pl.Utf8).str.strptime(pl.Date, '%Y-%m-%d', strict=False))
            .alias(c)
            for c in DATE_COLUMNS
        ]
    )


def main() -> None:
    inicio = time.time()
    
    if not SOURCE.exists():
        raise FileNotFoundError(f'No se encontró el archivo de origen: {SOURCE}')

    clean_raw_csv(SOURCE, CLEANED_RAW, DELETED_OUTPUT)

    print('Leyendo CSV limpio con Polars (lazy mode)...')
    df = pl.scan_csv(
        CLEANED_RAW,
        encoding='utf8',
        infer_schema_length=10000,
        truncate_ragged_lines=False,
        ignore_errors=False,
    )

    print('Normalizando centinelas...')
    df = df.with_columns(
        [
            pl.when(pl.col(c).cast(pl.Utf8).is_in(SENTINEL_STRINGS))
            .then(None)
            .otherwise(pl.col(c))
            .alias(c)
            for c in df.collect_schema().names()
        ]
    )
    
    print('Parseando columnas de fecha...')
    df = df.with_columns(
        [
            pl.when(pl.col(c).cast(pl.Utf8).is_in(SENTINEL_STRINGS))
            .then(None)
            .otherwise(pl.col(c).cast(pl.Utf8).str.strptime(pl.Date, '%Y-%m-%d', strict=False))
            .alias(c)
            for c in DATE_COLUMNS
        ]
    )

    print('Ejecutando operaciones y recolectando datos...')
    df = df.collect()
    print(f'Filas procesadas: {df.height:,}')

    print('Guardando dataset limpio...')
    df.write_csv(OUTPUT)
    print(f'✓ Limpieza completada. Archivo guardado como {OUTPUT}')
    
    # Guardar el tiempo de ejecución
    duracion = time.time() - inicio
    
    if not os.path.exists("Tiempos"):
        os.makedirs("Tiempos")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_tiempo = os.path.join("Tiempos", f"tiempo_ejecucion_limpiar_datos_{timestamp}.txt")
    
    with open(archivo_tiempo, "w") as f:
        f.write(f"Tiempo de ejecución de limpiar_datos.py\n")
        f.write(f"========================================\n")
        f.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duración: {duracion:.2f} segundos\n")
        f.write(f"Filas procesadas: {df.height:,}\n")
    
    print(f"Tiempo de ejecución guardado en: {archivo_tiempo}")


if __name__ == '__main__':
    main()