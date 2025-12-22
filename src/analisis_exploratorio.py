
# src/analisis_exploratorio.py
# ======================================================
# Herramientas para el análisis exploratorio sistemático de DataFrames en proyectos de Ciencia de Datos.
#
# Este módulo está diseñado para:
# - Realizar un análisis exploratorio inicial de cualquier DataFrame, clasificando y resumiendo las variables presentes.
# - Diferenciar y analizar tanto variables categóricas como numéricas.
# - Reportar valores faltantes de manera estructurada.
# - Visualizar información clave de los datos de manera reproducible y automática, ideal para notebooks o scripts.
# - Ofrecer un flujo rápido y seguro para obtener diagnósticos esenciales antes de limpiar o modelar los datos.
# ======================================================

# Importación de librerías principales
import pandas as pd  # Para manejo de DataFrames
import numpy as np   # Para operaciones numéricas
from IPython.display import display  # Para mostrar tablas en notebooks
from typing import List, Dict, Union  # Tipado estático

# Lista de funciones exportadas por el módulo
__all__ = [
     "analisis_exploratorio",
     "report_structure",
     "get_categorical_columns",
     "categorical_summary",
]



__all__ = [
    "analisis_exploratorio",
    "report_structure",
    "get_categorical_columns",
    "categorical_summary",
]


def report_structure(df: pd.DataFrame, show_head: int = 5) -> Dict:
    """
    Imprime y devuelve información básica: shape, dtypes y primeras filas.
    Parámetros:
        df (pd.DataFrame): DataFrame a analizar.
        show_head (int): número de filas a mostrar del head.
    Retorna:
        Dict: diccionario con 'shape', 'dtypes' y 'head'.
    """
    # Crea un diccionario con la información básica del DataFrame
    info = {
        "shape": df.shape,  # Dimensiones (filas, columnas)
        "dtypes": df.dtypes,  # Tipos de datos de cada columna
        "head": df.head(show_head)  # Primeras filas
    }
    # Imprime la estructura básica
    print("1) ESTRUCTURA BÁSICA")
    print("-" * 40)
    print(f"Dimensiones: {info['shape']}")
    print("\nTipos de datos:")
    print(info["dtypes"])
    print("\nPrimeras filas:")
    display(info["head"])
    # Devuelve el diccionario con la información
    return info


def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """
    Devuelve lista de columnas categóricas (object o category).
    Parámetros:
        df (pd.DataFrame): DataFrame a analizar.
    Retorna:
        List[str]: lista de nombres de columnas categóricas.
    """
    # Selecciona columnas de tipo object o category
    return df.select_dtypes(include=['object', 'category']).columns.tolist()


def categorical_summary(df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    """
    Devuelve DataFrame con número de valores únicos y top N valores + cuentas para cada columna categórica.
    Parámetros:
        df (pd.DataFrame): DataFrame a analizar.
        top_n (int): número de valores top a incluir.
    Retorna:
        pd.DataFrame: resumen categórico con columnas:
            - 'n_unique': número de valores únicos
            - 'top_values': lista de top N valores
            - 'top_counts': lista de cuentas correspondientes
    """
    cat_cols = get_categorical_columns(df)  # Obtiene columnas categóricas
    rows = []  # Lista para almacenar los resúmenes
    for c in cat_cols:
        vc = df[c].value_counts(dropna=False)  # Cuenta valores únicos
        top_values = vc.index[:top_n].tolist()  # Top N valores
        top_counts = vc.values[:top_n].tolist()  # Sus cuentas
        rows.append({
            "column": c,
            "n_unique": int(df[c].nunique(dropna=False)),
            "top_values": top_values,
            "top_counts": top_counts
        })
    # Devuelve el DataFrame resumen o vacío si no hay categóricas
    if rows:
        return pd.DataFrame(rows).set_index('column')
    else:
        return pd.DataFrame(columns=['n_unique', 'top_values', 'top_counts'])


def analisis_exploratorio(
    df: pd.DataFrame,
    nombre_df: str = "DataFrame",
    mostrar_head: int = 5,
    round_decimals: int = 2
) -> Dict:
    """
    Función principal de reporting para EDA.
    Llama a helpers (report_structure, categorical_summary) y muestra:
        - estructura, primeras filas
        - resumen de variables categóricas
        - resumen de variables numéricas
        - valores faltantes
    Retorna un dict con metadatos.
    Parámetros:
        df (pd.DataFrame): DataFrame a analizar.
        nombre_df (str): nombre descriptivo del DataFrame.
        mostrar_head (int): filas a mostrar en estructura.
        round_decimals (int): decimales para resumen numérico.
    Retorna:
        Dict: diccionario con resultados intermedios.
    """
    print(f"ANÁLISIS EXPLORATORIO DE {nombre_df.upper()}")
    print("=" * 50)

    resultados = {}  # Diccionario para almacenar resultados
    # 1. Estructura básica
    resultados['structure'] = report_structure(df, show_head=mostrar_head)

    # 2. Variables categóricas
    cat_cols = get_categorical_columns(df)
    resultados['categorical_columns'] = cat_cols
    if cat_cols:
        print("\n2) VARIABLES CATEGÓRICAS")
        print("-" * 40)
        print("Columnas categóricas:", cat_cols)
        resultados['categorical_summary'] = categorical_summary(df, top_n=3)
        display(resultados['categorical_summary'])
        # Mostrar top values concisos para cardinalidad pequeña
        for col in cat_cols:
            n_unique = df[col].nunique(dropna=False)
            print(f"\n- {col}: {n_unique} valores únicos")
            if n_unique <= 11:
                display(df[col].value_counts(dropna=False))

    # 3. Variables numéricas
    numericas = df.select_dtypes(include=[np.number])
    resultados['numeric_columns'] = numericas.columns.tolist()
    if not numericas.empty:
        print("\n3) VARIABLES NUMÉRICAS")
        print("-" * 40)
        print("Columnas numéricas:", resultados['numeric_columns'])
        display(numericas.describe().T.round(round_decimals))

    # 4. Valores faltantes
    print("\n4) VALORES FALTANTES")
    print("-" * 40)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    miss_df = pd.DataFrame({'missing_count': missing, 'missing_pct': missing_pct})
    resultados['missing'] = miss_df
    display(miss_df[miss_df['missing_count'] > 0].sort_values('missing_pct', ascending=False))

    # 5. Resumen final
    print("\n5) RESUMEN")
    print("-" * 40)
    print(f"Total registros: {len(df)}")
    print(f"Total columnas: {df.shape[1]}")

    return resultados



def calcular_tasa_proporciones(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """
    Calcula tasas de suscripción (y=1) por categoría.
    Parámetros:
        df (pd.DataFrame): DataFrame con columnas 'y' y la variable categórica.
        variable (str): Nombre de la columna categórica a analizar.
    Retorna:
        pd.DataFrame: con columnas [variable, total, exitos, fracasos, tasa_exito]
    """
    # Validación: la columna debe existir
    if variable not in df.columns:
        raise ValueError(f"Columna '{variable}' no existe. Columnas disponibles: {df.columns.tolist()}")
    # Validación: debe existir la columna 'y'
    if 'y' not in df.columns:
        raise ValueError("DataFrame debe contener columna 'y' (variable objetivo)")
    # Crea tabla de contingencia entre variable y target
    tabla = pd.crosstab(df[variable], df['y'], margins=False)
    # Construye el DataFrame resultado
    resultado = pd.DataFrame()
    resultado[variable] = tabla.index
    resultado['fracasos'] = tabla[0].values if 0 in tabla.columns else 0
    resultado['exitos'] = tabla[1].values if 1 in tabla.columns else 0
    resultado['total'] = resultado['fracasos'] + resultado['exitos']
    # Calcula la tasa de éxito como porcentaje
    resultado['tasa_exito'] = (
        resultado['exitos'].astype(float) / resultado['total'].astype(float)
    ) * 100
    # Devuelve el DataFrame resultado
    return resultado.reset_index(drop=True)