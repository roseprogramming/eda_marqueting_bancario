"""
PIPELINE: Carga → Limpia → Normaliza → Une → Exporta

Ejecutar desde terminal:
    .venv\\Scripts\\python.exe src/pipeline.py [--impute] [--profile]
"""

import pandas as pd
from pathlib import Path

# Importar funciones de limpieza existentes
from data_cleaning import clean_column_names
from cleaning_campaing import clean_campaign_df


# =============================================================================
# CARGA Y PROCESAMIENTO
# =============================================================================

def main(impute=False, profile=False):
    """Ejecuta el pipeline completo"""
    
    print("="*70)
    print("PIPELINE: Carga, Limpieza, Integración")
    print("="*70)
    
    # Crear carpeta de output
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    
    # 1. CARGAR CAMPAÑA CRUDA
    print("\n[1/5] Cargando campaña...")
    df_campaign = pd.read_csv('data/raw/bank-additional.csv', sep=',', index_col=0)
    print(f"  ✓ {df_campaign.shape[0]:,} registros × {df_campaign.shape[1]} columnas")
    
    # 2. LIMPIAR CAMPAÑA
    print("\n[2/5] Limpiando campaña...")
    df_campaign_clean = clean_campaign_df(df_campaign, impute=impute)
    print(f"  ✓ Campaña limpia y normalizada")
    
    # 3. GUARDAR CAMPAÑA LIMPIA
    df_campaign_clean.to_csv('data/processed/df_campaign_clean.csv', index=False)
    print(f"  ✓ Guardado: data/processed/df_campaign_clean.csv")
    
    # 4. CARGAR DETALLES CLIENTES (si --profile)
    if profile:
        print("\n[3/5] Cargando detalles clientes...")
        df_customers_list = []
        for year in ['2012', '2013', '2014']:
            try:
                df = pd.read_excel('data/raw/customer-details.xlsx', sheet_name=year, index_col=0)
                df['year'] = year
                df_customers_list.append(df)
                print(f"  ✓ {year}: {df.shape[0]:,} registros")
            except Exception as e:
                print(f"  ⚠ {year}: {e}")
        
        df_customers = pd.concat(df_customers_list, ignore_index=False)
        df_customers = df_customers.reset_index()
        df_customers.rename(columns={df_customers.columns[0]: 'id'}, inplace=True)
        
        # Normalizar nombres clientes
        df_customers = clean_column_names(df_customers, verbose=False)
        
        # Manualizar numwebvisitsmonth
        if 'numwebvisitsmonth' in df_customers.columns:
            df_customers = df_customers.rename(columns={'numwebvisitsmonth': 'num_web_visits_month'})
        
        df_customers.to_csv('data/processed/df_customer_details.csv', index=False)
        print(f"  ✓ Guardado: data/processed/df_customer_details.csv")
        
        # 5. UNIR CAMPAÑA + CLIENTES
        print("\n[4/5] Integrando datasets...")
        
        # Asegurar columna id en ambos
        if 'id' not in df_campaign_clean.columns and df_campaign_clean.index.name == 'id':
            df_campaign_clean = df_campaign_clean.reset_index()
        if 'id' not in df_customers.columns and df_customers.index.name == 'id':
            df_customers = df_customers.reset_index()
        
        # Merge
        df_perfil_cliente = pd.merge(df_campaign_clean, df_customers, on='id', how='inner')
        df_perfil_cliente = df_perfil_cliente.set_index('id')
        
        print(f"  ✓ Integrado: {df_perfil_cliente.shape[0]:,} registros × {df_perfil_cliente.shape[1]} columnas")
        
        # Guardar perfil
        df_perfil_cliente.to_csv('data/processed/df_perfil_cliente.csv', index=True)
        print(f"  ✓ Guardado: data/processed/df_perfil_cliente.csv")
        
        print("\n" + "="*70)
        print("✓ PIPELINE COMPLETADO CON ÉXITO")
        print("="*70)
        print(f"\nArchivos generados:")
        print(f"  • data/processed/df_campaign_clean.csv")
        print(f"  • data/processed/df_customer_details.csv")
        print(f"  • data/processed/df_perfil_cliente.csv ⭐ (USAR ESTE EN NOTEBOOK)")
    else:
        print("\n" + "="*70)
        print("✓ PIPELINE COMPLETADO (solo campaña)")
        print("="*70)
        print(f"\nArchivo generado:")
        print(f"  • data/processed/df_campaign_clean.csv")


if __name__ == '__main__':
    import sys
    
    impute = '--impute' in sys.argv
    profile = '--profile' in sys.argv
    
    main(impute=impute, profile=profile)
