df_campaign_clean = cc.clean_campaign_df(df_campaign)

def clean_campaign_df(df_campaign_original, impute: bool = False):







# src/cleaning_campaing.py
# ======================================================
# Módulo principal para la limpieza, transformación y preparación del DataFrame de campañas bancarias (`df_campaign`).
#
# Este módulo está diseñado para:
# - Limpieza y transformación estructurada del DataFrame según especificaciones del proyecto.
# - Normalización temporal: fechas, meses y años.
# - Corrección de tipos numéricos y separadores decimales.
# - Gestión de valores especiales y recodificación de variables clave.
# - Imputación de valores faltantes y tipado categórico.
# - Preparar un DataFrame listo para análisis y modelado.
# ======================================================

# Importación de librerías principales
import pandas as pd  # Para manejo de DataFrames
import numpy as np   # Para operaciones numéricas
import src.data_cleaning as dc  # Utilidades de limpieza genéricas

def clean_campaign_df(df_campaign_original, impute: bool = False):
    """
    Limpia y transforma el DataFrame de campañas bancarias (df_campaign).
    Permite desactivar imputaciones para EDA (impute=False por defecto).
    Parámetros:
        df_campaign_original (pd.DataFrame): DataFrame original con datos de la campaña.
        impute (bool): Si True, aplica imputaciones (mediana/moda) antes de castear.
    Retorna:
        pd.DataFrame: DataFrame limpio y listo para análisis/modelado.
    """
    # Crea una copia para no modificar el DataFrame original
    df = df_campaign_original.copy()
    
    # 1. Limpiar separadores decimales y convertir a float
    num_float = ['cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']
    for c in num_float:
        if c in df.columns:
            # 1.1 Limpieza y conversión a FLOAT
            df[c] = df[c].astype(str).str.replace(',', '.', regex=False)
            df[c] = pd.to_numeric(df[c], errors='coerce')
            # 1.2 Imputación opcional de NaNs (mediana)
            if impute and df[c].isnull().any():
                median_val = df[c].median()
                df[c] = df[c].fillna(median_val)
    
    # 2. Parsear y convertir columna 'date' (formato español)
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
    # Si existe la columna 'date', la convierte a datetime y extrae mes y año
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
    # Recodifica variables binarias mal tipadas
    for col in ['default', 'housing', 'loan']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.split(',').str[0]
            df[col] = df[col].replace({'nan': '0', 'unknown': '0', '0.0': '0', '1.0': '1'}).fillna('0')

    # 3.b Normalización de nombre de id
    if 'id_' in df.columns and 'id' not in df.columns:
        df = df.rename(columns={'id_': 'id'})

    # 4. Imputaciones y conversión a INT
    # A. Imputación opcional de 'age' (mediana escalar) y conversión a INT solo si no hay NaN
    if 'age' in df.columns:
        if impute and df['age'].isnull().any():
            age_median = df['age'].median()
            df['age'] = df['age'].fillna(age_median)
        if not df['age'].isnull().any():
            df['age'] = df['age'].astype(int)
    # B. Imputación por moda (solo 'education' en este punto, opcional)
    if impute:
        df = dc.impute_mode(df, ['education']) 

    # 5. Conversión final de binarias a INT
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

    # 8. Normalizar nombres de columnas a snake_case para coherencia
    try:
        df = dc.clean_column_names(df, verbose=True)
    except Exception:
        pass
    # Devuelve el DataFrame limpio y listo para análisis/modelado
    return df