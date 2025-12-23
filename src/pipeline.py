
"""
PIPELINE: Carga → Limpia → Normaliza → Une → Exporta
======================================================
Script principal para la preparación y consolidación de datos del proyecto EDA Marketing Bancario.

Este pipeline automatiza el flujo de trabajo que se hacía manualmente en el notebook en su primera versión, asegurando:
- Consistencia y reproducibilidad en la limpieza y unión de datos.
- Mantenimiento más sencillo y separación de responsabilidades.

------------------------------------------------------
EJECUCIÓN:
------------------------------------------------------
Desde terminal:
    .venv\\Scripts\\python.exe src/pipeline.py
Desde notebook:
    %run ../src/pipeline.py
------------------------------------------------------
"""


# Importación de librerías principales
import pandas as pd  # Para manejo de DataFrames
from pathlib import Path  # Para manipulación de rutas
import sys  # Para modificar el path de importación
import os   # Para operaciones de sistema


# Añade el directorio raíz del proyecto al sys.path para permitir imports relativos
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


# Importa funciones de limpieza de módulos propios
from src.data_cleaning import clean_column_names
from src.cleaning_campaing import clean_campaign_df



def main():
    """
    Ejecuta el pipeline completo replicando el flujo original del notebook en su primera versión.
    Flujo:
        1. Cargar raw data con index_col=0 (ignora Unnamed:0)
        2. Limpiar campaña con clean_campaign_df() + clean_column_names()
        3. Guardar df_campaign_clean.csv (24 cols, id como columna)
        4. Concatenar customers con keys=['2012','2013','2014'] + reset_index(level=0)
        5. Normalizar customers con clean_column_names() + rename numwebvisitsmonth
        6. Guardar df_customer_details.csv (7 cols, id como columna)
        7. Merge con left_on='id', right_on='id', how='inner'
        8. set_index('id') para establecer UUID como índice
        9. Guardar df_perfil_cliente.csv (43,000 × 29, índice=UUID)
    """
    # Imprime cabecera del pipeline
    print("="*70)
    print("PIPELINE: Carga, Limpieza, Integración")
    print("="*70)
    
    # Crea la carpeta de salida si no existe
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    
    # 1. CARGAR CAMPAÑA CRUDA
    print("\n[1/8] Cargando campaña...")
    df_campaign = pd.read_csv('data/raw/bank-additional.csv', index_col=0)  # Lee el archivo CSV de campaña
    print(f"  ✓ {df_campaign.shape[0]:,} registros × {df_campaign.shape[1]} columnas")
    
    # 2. EXPLORAR DATOS CRUDOS (opcional)
    print("\n[2/8] Estructura del dataset crudo:")
    print(f"  Columnas: {list(df_campaign.columns)[:5]}... ({len(df_campaign.columns)} total)")
    
    # 3. LIMPIAR CAMPAÑA
    print("\n[3/8] Limpiando campaña...")
    df_campaign_clean = clean_campaign_df(df_campaign)  # Aplica limpieza específica de campaña
    print("  ✓ Módulo cleaning_campaing aplicado correctamente")
    
    df_campaign_clean = clean_column_names(df_campaign_clean, verbose=True)  # Normaliza nombres de columnas
    print("  ✓ Limpieza de df_campaign completada")
    
    # 4. GUARDAR df_campaign_clean.csv
    df_campaign_clean.to_csv('data/processed/df_campaign_clean.csv', index=False)  # Guarda el DataFrame limpio
    print(f"  ✓ Guardado: data/processed/df_campaign_clean.csv")
    
    # 5. CARGAR Y CONCATENAR CUSTOMERS
    print("\n[4/8] Cargando detalles clientes...")
    # Carga los datos de clientes de cada año
    df_customer_2012 = pd.read_excel('data/raw/customer-details.xlsx', sheet_name='2012', index_col=0)  # Carga clientes 2012
    df_customer_2013 = pd.read_excel('data/raw/customer-details.xlsx', sheet_name='2013', index_col=0)  # Carga clientes 2013
    df_customer_2014 = pd.read_excel('data/raw/customer-details.xlsx', sheet_name='2014', index_col=0)  # Carga clientes 2014
    print(f"  ✓ 2012: {df_customer_2012.shape[0]:,} registros")
    print(f"  ✓ 2013: {df_customer_2013.shape[0]:,} registros")
    print(f"  ✓ 2014: {df_customer_2014.shape[0]:,} registros")
    # Combina los DataFrames usando keys para mantener el año
    print("\n[5/8] Combinando DataFrames de clientes...")
    df_customer_years = pd.concat(
        [df_customer_2012, df_customer_2013, df_customer_2014],  # Lista de DataFrames de clientes
        keys=['2012', '2013', '2014'],  # Etiquetas de año
        axis=0  # Concatenación vertical
    )
    # Resetea el índice para convertir el año en columna
    df_customer_details = df_customer_years.reset_index(level=0)  # Etiqueta de año pasa a ser columna
    df_customer_details.rename(columns={'level_0': 'year'}, inplace=True)  # Renombra columna de año
    print("  ✓ DataFrames combinados con columna 'year'")
    
    # 6. NORMALIZAR CUSTOMERS
    print("\n[6/8] Normalizando nombres de columnas...")
    df_customer_details = clean_column_names(df_customer_details, verbose=True)  # Normaliza nombres de columnas
    # Renombra manualmente la columna si existe
    if 'numwebvisitsmonth' in df_customer_details.columns:
        df_customer_details.rename(columns={'numwebvisitsmonth': 'num_web_visits_month'}, inplace=True)
        print("  ✓ Columna 'numwebvisitsmonth' renombrada a 'num_web_visits_month'")
    print("  ✓ DataFrames combinados y normalizados correctamente")
    
    # 7. GUARDAR df_customer_details.csv
    df_customer_details.to_csv('data/processed/df_customer_details.csv', index=False)
    print(f"  ✓ Guardado: data/processed/df_customer_details.csv")
    
    # 8. MERGE de campañas y clientes
    print("\n[7/8] Integrando datasets (merge campaña + clientes por columna 'id')...")
    # Une los DataFrames usando la columna 'id'
    df_perfil_cliente = pd.merge(
        df_campaign_clean,       # Tabla izquierda (campaña)
        df_customer_details,     # Tabla derecha (detalles cliente)
        left_on='id',            # Columna clave izquierda
        right_on='id',           # Columna clave derecha
        how='inner'              # Solo registros coincidentes
    )
   
    df_perfil_cliente.set_index('id', inplace=True)  # Establece 'id' como índice
    df_perfil_cliente.index.name = None  # Elimina el nombre del índice
    print(f"  ✓ Combinación completada: {df_perfil_cliente.shape[0]:,} registros × {df_perfil_cliente.shape[1]} columnas")
    
    # 9. GUARDAR df_perfil_cliente.csv
    print("\n[8/8] Guardando dataset final...")
    df_perfil_cliente.to_csv('data/processed/df_perfil_cliente.csv', index=True)  # Guarda el DataFrame final
    print(f"  ✓ Guardado: data/processed/df_perfil_cliente.csv")
    
    # RESUMEN FINAL
    print("\n" + "="*70)
    print("✓ PIPELINE COMPLETADO CON ÉXITO")
    print("="*70)
    print(f"\nArchivos generados en data/processed/:")
    # Imprime resumen de archivos generados con numero de filas (registros) y columnas
    print(f"  • df_campaign_clean.csv    ({df_campaign_clean.shape[0]:,} × {df_campaign_clean.shape[1]})")
    print(f"  • df_customer_details.csv  ({df_customer_details.shape[0]:,} × {df_customer_details.shape[1]})")
    print(f"  • df_perfil_cliente.csv    ({df_perfil_cliente.shape[0]:,} × {df_perfil_cliente.shape[1]}) ★")
    print("\n→ Usar df_perfil_cliente.csv para análisis en notebook")
    return df_perfil_cliente



# Punto de entrada del script
if __name__ == '__main__':
    main()
