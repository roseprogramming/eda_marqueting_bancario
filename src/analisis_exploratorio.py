# src/analisis_exploratorio.py
import pandas as pd
import numpy as np
from IPython.display import display
from typing import List, Dict, Union
"""
Módulo: analisis_exploratorio.py
======================================================

Herramientas para el análisis exploratorio sistemático de DataFrames en proyectos de Ciencia de Datos.

Este módulo está diseñado para:
- Realizar un análisis exploratorio inicial de cualquier DataFrame, clasificando y resumiendo las variables presentes.
- Diferenciar y analizar tanto variables categóricas como numéricas.
- Reportar valores faltantes de manera estructurada.
- Visualizar información clave de los datos de manera reproducible y automática, ideal para notebooks o scripts.
- Ofrecer un flujo rápido y seguro para obtener diagnósticos esenciales antes de limpiar o modelar los datos.

------------------------------------------------------
FUNCIONES DISPONIBLES EN ESTE MÓDULO:
------------------------------------------------------

1) report_structure(df, show_head=5)
   - Imprime y devuelve información básica del DataFrame: dimensiones, tipos de datos y primeras filas.
   - Argumentos:
       df: DataFrame a analizar.
       show_head (int): filas de ejemplo a mostrar.
   - Retorna: dict con 'shape', 'dtypes' y 'head'.

2) get_categorical_columns(df)
   - Devuelve una lista con los nombres de las columnas categóricas (object o category).

3) categorical_summary(df, top_n=3)
   - Devuelve un DataFrame resumen con número de valores únicos y los top N valores y sus cuentas
     para cada columna categórica detectada en el DataFrame.

4) analisis_exploratorio(df, nombre_df="DataFrame", mostrar_head=5, round_decimals=2)
   - Función principal que organiza y muestra:
     - Estructura básica (report_structure)
     - Resumen de variables categóricas (categorical_summary)
     - Resumen de variables numéricas (describe)
     - Tabla de valores faltantes con porcentajes
   - Retorna un dict con los resultados intermedios (estructura, listas de columnas, missing, etc.).

------------------------------------------------------
BUENAS PRÁCTICAS/TIPS:
------------------------------------------------------
- Llama a analisis_exploratorio(df) tras cargar un DataFrame para una inspección rápida.
- Este módulo se centra en reporting; NO debe mutar el DataFrame de entrada.
- Para transformaciones (coerciones, imputaciones), utiliza src.data_cleaning, para utiliza visualizaciones src.plotting.

------------------------------------------------------
EJEMPLO DE USO EN NOTEBOOK:
------------------------------------------------------
from src.analisis_exploratorio import analisis_exploratorio
analisis_exploratorio(df_mis_datos, nombre_df="Datos de Clientes")
"""



__all__ = [
    "analisis_exploratorio",
    "report_structure",
    "get_categorical_columns",
    "categorical_summary",
]

def report_structure(df: pd.DataFrame, show_head: int = 5) -> Dict:
    """Imprime y devuelve información básica: shape, dtypes y primeras filas.
    args:
        df (pd.DataFrame): DataFrame a analizar.
        show_head (int): número de filas a mostrar del head.
    returns:
        Dict: diccionario con 'shape', 'dtypes' y 'head'."""
        
    info = {
        "shape": df.shape,
        "dtypes": df.dtypes,
        "head": df.head(show_head)
    }
    print("1) ESTRUCTURA BÁSICA")
    print("-" * 40)
    print(f"Dimensiones: {info['shape']}")
    print("\nTipos de datos:")
    print(info["dtypes"])
    print("\nPrimeras filas:")
    display(info["head"])
    return info

def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """Devuelve lista de columnas categóricas (object o category).
    args:
        df (pd.DataFrame): DataFrame a analizar.
    returns:
        List[str]: lista de nombres de columnas categóricas."""
    
    return df.select_dtypes(include=['object', 'category']).columns.tolist()

def categorical_summary(df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    """
    Devuelve DataFrame con número de valores únicos y top N valores + cuentas
    para cada columna categórica.
    args:
        df (pd.DataFrame): DataFrame a analizar.
        top_n (int): número de valores top a incluir.
    returns:
        pd.DataFrame: resumen categórico con columnas:
            - 'n_unique': número de valores únicos
            - 'top_values': lista de top N valores
            - 'top_counts': lista de cuentas correspondientes
    """
    cat_cols = get_categorical_columns(df)
    rows = []
    for c in cat_cols:
        vc = df[c].value_counts(dropna=False)
        top_values = vc.index[:top_n].tolist()
        top_counts = vc.values[:top_n].tolist()
        rows.append({
            "column": c,
            "n_unique": int(df[c].nunique(dropna=False)),
            "top_values": top_values,
            "top_counts": top_counts
        })
    if rows:
        return pd.DataFrame(rows).set_index('column')
    else:
        return pd.DataFrame(columns=['n_unique', 'top_values', 'top_counts'])

def analisis_exploratorio(df: pd.DataFrame,
                          nombre_df: str = "DataFrame",
                          mostrar_head: int = 5,
                          round_decimals: int = 2) -> Dict:
    """
    Función principal de reporting para EDA.
    Llama a helpers (report_structure, categorical_summary) y muestra:
    - estructura, primeras filas
    - resumen de variables categóricas
    - resumen de variables numéricas
    - valores faltantes
    Retorna un dict con metadatos.
    args:
        df (pd.DataFrame): DataFrame a analizar.
        nombre_df (str): nombre descriptivo del DataFrame.
        mostrar_head (int): filas a mostrar en estructura.
        round_decimals (int): decimales para resumen numérico.
    returns:
        Dict: diccionario con resultados intermedios.  
    """
    print(f"ANÁLISIS EXPLORATORIO DE {nombre_df.upper()}")
    print("=" * 50)

    resultados = {}
    # estructura básica
    resultados['structure'] = report_structure(df, show_head=mostrar_head)

    # categóricas
    cat_cols = get_categorical_columns(df)
    resultados['categorical_columns'] = cat_cols
    if cat_cols:
        print("\n2) VARIABLES CATEGÓRICAS")
        print("-" * 40)
        print("Columnas categóricas:", cat_cols)
        resultados['categorical_summary'] = categorical_summary(df, top_n=3)
        display(resultados['categorical_summary'])
        # mostrar top values concisos para cardinalidad pequeña
        for col in cat_cols:
            n_unique = df[col].nunique(dropna=False)
            print(f"\n- {col}: {n_unique} valores únicos")
            if n_unique <= 11:
                display(df[col].value_counts(dropna=False))

    # numéricas
    numericas = df.select_dtypes(include=[np.number])
    resultados['numeric_columns'] = numericas.columns.tolist()
    if not numericas.empty:
        print("\n3) VARIABLES NUMÉRICAS")
        print("-" * 40)
        print("Columnas numéricas:", resultados['numeric_columns'])
        display(numericas.describe().T.round(round_decimals))

    # faltantes
    print("\n4) VALORES FALTANTES")
    print("-" * 40)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    miss_df = pd.DataFrame({'missing_count': missing, 'missing_pct': missing_pct})
    resultados['missing'] = miss_df
    display(miss_df[miss_df['missing_count'] > 0].sort_values('missing_pct', ascending=False))

    # resumen
    print("\n5) RESUMEN")
    print("-" * 40)
    print(f"Total registros: {len(df)}")
    print(f"Total columnas: {df.shape[1]}")

    return resultados


def calcular_tasa_proporciones(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """
    Calcula tasas de suscripción (y=1) por categoría.
    
    Args:
        df: DataFrame con columnas 'y' y 'variable'
        variable: Nombre de la columna categórica a analizar
    
    Returns:
        DataFrame con columnas: [variable, total, exitos, fracasos, tasa_exito]
    
    Raises:
        ValueError: Si falta alguna columna requerida
    
    Example:
        >>> tasa = calcular_tasa_proporciones(df, 'education')
        >>> print(tasa.sort_values('tasa_exito', ascending=False))
    """
    # Validaciones
    if variable not in df.columns:
        raise ValueError(f"Columna '{variable}' no existe. Columnas disponibles: {df.columns.tolist()}")
    
    if 'y' not in df.columns:
        raise ValueError("DataFrame debe contener columna 'y' (variable objetivo)")
    
    # Crear tabla de contingencia
    tabla = pd.crosstab(df[variable], df['y'], margins=False)
    
    # Construir resultado
    resultado = pd.DataFrame()
    resultado[variable] = tabla.index
    resultado['fracasos'] = tabla[0].values if 0 in tabla.columns else 0
    resultado['exitos'] = tabla[1].values if 1 in tabla.columns else 0
    resultado['total'] = resultado['fracasos'] + resultado['exitos']
    
    # Conversión explícita para evitar warnings de tipo
    resultado['tasa_exito'] = (
        resultado['exitos'].astype(float) / resultado['total'].astype(float)
    ) * 100
    
    return resultado.reset_index(drop=True)