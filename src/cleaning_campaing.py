# src/cleaning_campaing.py
import pandas as pd
import numpy as np
import src.data_cleaning as dc
"""
Módulo: cleaning_campaign.py
======================================================
Módulo principal para la limpieza, transformación y preparación del DataFrame de campañas bancarias (`df_campaign`) para las etapas de análisis y modelado.
------------------------------------------------------
Este módulo está diseñado para:
- **Limpieza y transformación estructurada** del DataFrame según especificaciones del proyecto (tipos, valores especiales, formato de fechas y variables categóricas).
- **Normalización Temporal**: Extrae, limpia y tipa correctamente fechas, meses y años para análisis longitudinal y de estacionalidad.
- **Corrección de Tipos Numéricos**: Corrige objetos mal tipados (ej. valores macroeconómicos) debido a separadores decimales incorrectos (comas).
- **Gestión de Valores Especiales**: Recodifica marcadores como `999` en `pdays` y el target binario `y` (`yes`/`no` → `1`/`0`).
- **Imputación de Valores Faltantes**: Aplica estrategias de imputación (mediana para numéricas, moda para categóricas) a columnas críticas.
- **Asegurar Calidad**: Prepara un DataFrame estructuralmente correcto y listo para ser consumido por módulos de visualización y *machine learning*.
------------------------------------------------------
FUNCIONES DISPONIBLES EN ESTE MÓDULO:
------------------------------------------------------
1) clean_campaign_df(df_campaign_original)
    - Función principal que aplica la secuencia completa de limpieza y transformación del DataFrame de la campaña bancaria.
    - Pasos incluidos: corrección de separadores, conversión a `datetime`, recodificación de `pdays` y target `y`, imputación y tipado categórico.
    - Argumentos:
        df_campaign_original (pd.DataFrame): DataFrame original (sin modificar) con los datos de la campaña.
    - Retorna: pd.DataFrame limpio y listo para análisis/modelado.
------------------------------------------------------
BUENAS PRÁCTICAS/TIPS:
------------------------------------------------------
- **Inmutabilidad:** La lógica de la función `clean_campaign_df` debe usar una copia (`df.copy()`) del DataFrame de entrada para no mutar el original.
- **Validación:** Posterior a la limpieza, se recomienda la validación con `run_checks()` o una inspección visual para asegurar la calidad.
- **Modularidad:** Para utilidades de limpieza más genéricas y reusables (ej. manejo de NaNs), basarse en el módulo `src.data_cleaning`.
------------------------------------------------------
EJEMPLO DE USO EN NOTEBOOK:
------------------------------------------------------
import cleaning_campaign as cc
import pandas as pd
# Suponiendo que df_campaign ya está cargado
df_campaign_clean = cc.clean_campaign_df(df_campaign)
print(df_campaign_clean.head())

"""

def clean_campaign_df(df_campaign_original):
    """
    Limpia y transforma el DataFrame de campañas bancarias (df_campaign).
    Asegura tipos correctos para 'age' (int) y variables macro (float) 
    y gestiona NaNs y valores especiales como 999 en 'pdays'.
    Args:
        df_campaign_original (pd.DataFrame): DataFrame original con datos de la campaña.
    Returns:
        pd.DataFrame: DataFrame limpio y listo para análisis/modelado.
    """
    df = df_campaign_original.copy()
    
    # 1. Limpiar separadores decimales, convertir a FLOAT, e IMPUTAR MEDIANA (Manual)
    num_float = ['cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']
    for c in num_float:
        if c in df.columns:
            # 1.1 Limpieza y conversión a FLOAT
            df[c] = df[c].astype(str).str.replace(',', '.', regex=False)
            df[c] = pd.to_numeric(df[c], errors='coerce')
            
            # 1.2 Imputación de NaNs de FLOAT (Manual con valor escalar)
            if df[c].isnull().any():
                median_val = df[c].median()
                df[c] = df[c].fillna(median_val)
    
    # 2. Parsear y convertir columna 'date' (SIN CAMBIOS)
    meses_es = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
                'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
    def parse_fecha_es(fecha):
        if pd.isna(fecha): return np.nan
        partes = str(fecha).strip().split('-')
        if len(partes) != 3: return np.nan
        try:
            dia = int(partes[0])
            mes = meses_es[partes[1].lower()]
            anio = int(partes[2])
            return f"{anio}-{mes:02d}-{dia:02d}"
        except Exception:
            return np.nan
            
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'].apply(parse_fecha_es), format='%Y-%m-%d', errors='coerce')
        df['contact_month'] = df['date'].dt.month.astype('Int64')
        df['contact_year'] = df['date'].dt.year.astype('Int64')

    # 3. Recodificar target 'y', 'pdays', y preparar binarias
    if 'y' in df.columns:
        df['y'] = df['y'].map({'yes':1, 'no':0})
    if 'pdays' in df.columns:
        df['previous_contact'] = (df['pdays'] < 999).astype(int)
        df.loc[df['pdays'] == 999, 'pdays'] = np.nan
        
    for col in ['default', 'housing', 'loan']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.split(',').str[0]
            df[col] = df[col].replace({'nan': '0', 'unknown': '0', '0.0': '0', '1.0': '1'}).fillna('0')

    # 4. Imputaciones y Conversión a INT
    
    # A. Imputación MANUAL de 'age' (MEDIANA ESCALAR y Conversión a INT)
    if 'age' in df.columns:
        if df['age'].isnull().any():
            # **CORRECCIÓN DEL IntCastingNaNError**
            age_median = df['age'].median() # <-- Usamos mediana para obtener un escalar
            df['age'] = df['age'].fillna(age_median)
        df['age'] = df['age'].astype(int) 

    # B. Imputación por moda (solo 'education' en este punto)
    df = dc.impute_mode(df, ['education']) 
    
    # 5. CONVERSIÓN FINAL DE BINARIAS A INT
    for col in ['default', 'housing', 'loan']:
        if col in df.columns:
            df[col] = df[col].astype(int) 

    # 6. Forzar tipo category a columnas categóricas conocidas
    cats = ['job','marital','education','contact_month','contact_year','default','housing','loan']
    cats = [c for c in cats if c in df.columns]
    df = dc.coerce_to_category(df, cats)
    
    # 7. Eliminar columnas geográficas incorrectas (descontextualizadas)
    for c in ['lat', 'latitude', 'longitude', 'long']:
        if c in df.columns:
            df = df.drop(columns=c)
    
    return df