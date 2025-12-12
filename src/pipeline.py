"""
PIPELINE: Carga → Limpia → Normaliza → Une → Exporta

Se decide implementar un pipeline completo en un solo script para replicar
el flujo original del notebook de análisis exploratorio en el cual se realizaba este proceso en varias etapas y en diferentes celdas.
Con este cambio aseguramos la consistencia y reproducibilidad del proceso de preparación de datos asi como simplificamos el mantenimiento y obtenemos un notebook más limpio y con menos responsabilidades.

Ejecutar desde terminal:
    .venv\\Scripts\\python.exe src/pipeline.py

Ejecutar desde notebook:
    %run ../src/pipeline.py
"""

import pandas as pd
from pathlib import Path
import sys
import os

# Añadir el directorio raíz del proyecto al path para imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Importar funciones de limpieza existentes
from src.data_cleaning import clean_column_names
from src.cleaning_campaing import clean_campaign_df


def main():
    """
    Ejecuta el pipeline completo replicando el flujo original del notebook.
    
    Flujo:
    1. Cargar raw data con index_col=0 (ignora Unnamed:0)
    2. Limpiar campaña con cc.clean_campaign_df() + dc.clean_column_names()
    3. Guardar df_campaign_clean.csv (24 cols, id como columna)
    4. Concatenar customers con keys=['2012','2013','2014'] + reset_index(level=0)
    5. Normalizar customers con dc.clean_column_names() + rename numwebvisitsmonth
    6. Guardar df_customer_details.csv (7 cols, id como columna)
    7. Merge con left_on='id', right_on='id', how='inner'
    8. set_index('id') para establecer UUID como índice
    9. Guardar df_perfil_cliente.csv (43,000 × 29, índice=UUID)
    """
    
    print("="*70)
    print("PIPELINE: Carga, Limpieza, Integración")
    print("="*70)
    
    # Crear carpeta de output
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    
    # =========================================================================
    # 1. CARGAR CAMPAÑA CRUDA (con index_col=0 como en el notebook original)
    # =========================================================================
    print("\n[1/8] Cargando campaña...")
    df_campaign = pd.read_csv('data/raw/bank-additional.csv', index_col=0)
    print(f"  ✓ {df_campaign.shape[0]:,} registros × {df_campaign.shape[1]} columnas")
    
    # =========================================================================
    # 2. EXPLORAR DATOS CRUDOS (opcional - solo print)
    # =========================================================================
    print("\n[2/8] Estructura del dataset crudo:")
    print(f"  Columnas: {list(df_campaign.columns)[:5]}... ({len(df_campaign.columns)} total)")
    
    # =========================================================================
    # 3. LIMPIAR CAMPAÑA con clean_campaign_df() + clean_column_names()
    # =========================================================================
    print("\n[3/8] Limpiando campaña...")
    df_campaign_clean = clean_campaign_df(df_campaign)
    print("  ✓ Módulo cleaning_campaing aplicado correctamente")
    
    # Normalización de nombres de columnas según estándar PEP 8 (snake_case)
    df_campaign_clean = clean_column_names(df_campaign_clean, verbose=True)
    print("  ✓ Limpieza de df_campaign completada")
    
    # =========================================================================
    # 4. GUARDAR df_campaign_clean.csv (ID es columna, no índice)
    # =========================================================================
    df_campaign_clean.to_csv('data/processed/df_campaign_clean.csv', index=False)
    print(f"  ✓ Guardado: data/processed/df_campaign_clean.csv")
    
    # =========================================================================
    # 5. CARGAR Y CONCATENAR CUSTOMERS con keys= + reset_index(level=0)
    # =========================================================================
    print("\n[4/8] Cargando detalles clientes...")
    
    # Cargar cada año con index_col=0 (como en el notebook original)
    df_customer_2012 = pd.read_excel('data/raw/customer-details.xlsx', sheet_name='2012', index_col=0)
    df_customer_2013 = pd.read_excel('data/raw/customer-details.xlsx', sheet_name='2013', index_col=0)
    df_customer_2014 = pd.read_excel('data/raw/customer-details.xlsx', sheet_name='2014', index_col=0)
    
    print(f"  ✓ 2012: {df_customer_2012.shape[0]:,} registros")
    print(f"  ✓ 2013: {df_customer_2013.shape[0]:,} registros")
    print(f"  ✓ 2014: {df_customer_2014.shape[0]:,} registros")
    
    # Combinación usando keys para mantener año como MultiIndex (FLUJO ORIGINAL)
    print("\n[5/8] Combinando DataFrames de clientes...")
    df_customer_years = pd.concat(
        [df_customer_2012, df_customer_2013, df_customer_2014],
        keys=['2012', '2013', '2014'],
        axis=0
    )
    
    # Reseteo de índice para análisis y conversión de la clave año en columna
    df_customer_details = df_customer_years.reset_index(level=0)
    df_customer_details.rename(columns={'level_0': 'year'}, inplace=True)
    print("  ✓ DataFrames combinados con columna 'year'")
    
    # =========================================================================
    # 6. NORMALIZAR CUSTOMERS con clean_column_names()
    # =========================================================================
    print("\n[6/8] Normalizando nombres de columnas...")
    df_customer_details = clean_column_names(df_customer_details, verbose=True)
    
    # Normalización manual adicional de la columna numwebvisitsmonth
    if 'numwebvisitsmonth' in df_customer_details.columns:
        df_customer_details.rename(columns={'numwebvisitsmonth': 'num_web_visits_month'}, inplace=True)
        print("  ✓ Columna 'numwebvisitsmonth' renombrada a 'num_web_visits_month'")
    
    print("  ✓ DataFrames combinados y normalizados correctamente")
    
    # =========================================================================
    # 7. GUARDAR df_customer_details.csv (ID es columna, no índice)
    # =========================================================================
    df_customer_details.to_csv('data/processed/df_customer_details.csv', index=False)
    print(f"  ✓ Guardado: data/processed/df_customer_details.csv")
    
    # =========================================================================
    # 8. MERGE con left_on='id', right_on='id' (FLUJO ORIGINAL)
    # =========================================================================
    print("\n[7/8] Integrando datasets (merge campaña + clientes por columna 'id')...")
    
    # Unir los DataFrames usando la columna 'id' (normalizada por clean_column_names)
    # clean_column_names() convierte id_ → id y ID → id
    df_perfil_cliente = pd.merge(
        df_campaign_clean,       # Tabla izquierda (campaña)
        df_customer_details,     # Tabla derecha (detalles cliente)
        left_on='id',
        right_on='id',
        how='inner'
    )
    
    # Establecer 'id' como índice (como en el notebook original)
    df_perfil_cliente.set_index('id', inplace=True)
    df_perfil_cliente.index.name = None
    
    print(f"  ✓ Combinación completada: {df_perfil_cliente.shape[0]:,} registros × {df_perfil_cliente.shape[1]} columnas")
    
    # =========================================================================
    # 9. GUARDAR df_perfil_cliente.csv
    # =========================================================================
    print("\n[8/8] Guardando dataset final...")
    df_perfil_cliente.to_csv('data/processed/df_perfil_cliente.csv', index=True)
    print(f"  ✓ Guardado: data/processed/df_perfil_cliente.csv")
    
    # =========================================================================
    # RESUMEN FINAL
    # =========================================================================
    print("\n" + "="*70)
    print("✓ PIPELINE COMPLETADO CON ÉXITO")
    print("="*70)
    print(f"\nArchivos generados en data/processed/:")
    print(f"  • df_campaign_clean.csv    ({df_campaign_clean.shape[0]:,} × {df_campaign_clean.shape[1]})")
    print(f"  • df_customer_details.csv  ({df_customer_details.shape[0]:,} × {df_customer_details.shape[1]})")
    print(f"  • df_perfil_cliente.csv    ({df_perfil_cliente.shape[0]:,} × {df_perfil_cliente.shape[1]}) ⭐")
    print("\n→ Usar df_perfil_cliente.csv para análisis en notebook")
    
    return df_perfil_cliente


if __name__ == '__main__':
    main()
