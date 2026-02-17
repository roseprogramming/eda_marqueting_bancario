
"""
Módulo: data_cleaning.py
======================================================
Herramientas para la limpieza y transformación de DataFrames en proyectos de Ciencia de Datos.

Este módulo está diseñado para:
- Realizar transformaciones de tipos de datos (coerciones a category).
- Imputar valores faltantes usando diferentes estrategias (mediana, moda).
- Proporcionar un wrapper (run_checks) que combina transformaciones y puede delegar el reporting a analisis_exploratorio.py.

------------------------------------------------------
FUNCIONES DISPONIBLES EN ESTE MÓDULO:
------------------------------------------------------
1) coerce_to_category(df, columns, inplace=False)
2) impute_median(df, columns, inplace=False)
3) impute_mode(df, columns, inplace=False)
4) run_checks(df, posibles_cat=None, inplace=False, call_analisis=False)
------------------------------------------------------
BUENAS PRÁCTICAS/TIPS:
------------------------------------------------------
- Este módulo se centra en transformaciones (NO en reporting).
- Para análisis exploratorio y visualización, usar src.analisis_exploratorio y src.plotting.
- Las funciones son puras: si inplace=False, retornan nuevo DataFrame sin modificar el original.
- Preferir call_analisis=True en run_checks() si necesitas tanto transformación como reporting.
------------------------------------------------------
EJEMPLO DE USO EN NOTEBOOK:
------------------------------------------------------
import src.data_cleaning as dc
# Solo transformación
df_clean = dc.coerce_to_category(df, ['education', 'marital'])
df_clean = dc.impute_median(df_clean, ['age', 'balance'])
# Transformación + reporting
results = dc.run_checks(df, posibles_cat=['education', 'marital'], call_analisis=True)
df_processed = results['df']
"""


# Importación de librerías principales
import pandas as pd  # Para manejo de DataFrames
import numpy as np   # Para operaciones numéricas
import re  # Para expresiones regulares (usado en limpiar_nombres_columnas)
from typing import List, Dict, Union, Optional  # Tipado estático


# Lista de funciones exportadas por el módulo
__all__ = [
    "forzar_a_categoria",
    "imputar_mediana", 
    "imputar_moda",
    "ejecutar_chequeos",
    "limpiar_nombres_columnas"
]


def forzar_a_categoria(df: pd.DataFrame, columns: List[str], inplace: bool = False) -> pd.DataFrame:
    """
    Convierte columnas especificadas al tipo category.
    Parámetros:
        df (pd.DataFrame): DataFrame a modificar.
        columns (List[str]): Lista de columnas a convertir.
        inplace (bool): Si True, modifica el df original; si False, retorna una copia.
    Retorna:
        pd.DataFrame: DataFrame con conversiones aplicadas.
    """
    # Si inplace es False, crea una copia para no modificar el original
    if not inplace:
        df = df.copy()
    # Itera sobre cada columna especificada
    # 'columns or []' asegura que si columns es None o vacío, no se itera y se evita error.
    for c in columns or []:
        # Si la columna existe en el DataFrame
        if c in df.columns:
            # Convierte la columna al tipo category
            df[c] = df[c].astype('category')
    # Devuelve el DataFrame modificado
    return df


def imputar_mediana(df: pd.DataFrame, columns: List[str], inplace: bool = False) -> pd.DataFrame:
    """
    Imputa la mediana en columnas numéricas especificadas.
    Parámetros:
        df (pd.DataFrame): DataFrame a modificar.
        columns (List[str]): Lista de columnas para imputar.
        inplace (bool): Si True, modifica el df original; si False, retorna una copia.
    Retorna:
        pd.DataFrame: DataFrame con imputaciones aplicadas.
    """
    # Si inplace es False, crea una copia para no modificar el original
    if not inplace:
        df = df.copy()
    # Itera sobre cada columna especificada
    # 'columns or []' asegura que si columns es None o vacío, no se itera y se evita error.
    for c in columns or []:
        # Si la columna existe y es numérica
        if c in df.columns and pd.api.types.is_numeric_dtype(df[c]):
            # Imputa la mediana en los valores nulos
            df[c] = df[c].fillna(df[c].median())
    # Devuelve el DataFrame modificado
    return df


def imputar_moda(df: pd.DataFrame, columns: List[str], inplace: bool = False) -> pd.DataFrame:
    """
    Imputa la moda en columnas especificadas.
    Parámetros:
        df (pd.DataFrame): DataFrame a modificar.
        columns (List[str]): Lista de columnas para imputar.
        inplace (bool): Si True, modifica el df original; si False, retorna una copia.
    Retorna:
        pd.DataFrame: DataFrame con imputaciones aplicadas.
    """
    # Si inplace es False, crea una copia para no modificar el original
    if not inplace:
        df = df.copy()
    # Itera sobre cada columna especificada
    # 'columns or []' asegura que si columns es None o vacío, no se itera y se evita error.
    for c in columns or []:
        # Si la columna existe
        if c in df.columns:
            # Calcula la moda (valor más frecuente)
            mode = df[c].mode(dropna=True)
            # Si hay moda, imputa ese valor en los nulos
            if not mode.empty:
                df[c] = df[c].fillna(mode.iloc[0])
    # Devuelve el DataFrame modificado
    return df


def ejecutar_chequeos(
    df: pd.DataFrame,
    posibles_cat: Optional[List[str]] = None,
    inplace: bool = False,
    call_analisis: bool = False
) -> Dict:
    """
    Wrapper que combina transformaciones y puede llamar a analisis_exploratorio.
    Retorna dict con resultados y DataFrame procesado.
    Parámetros:
        df (pd.DataFrame): DataFrame a procesar.
        posibles_cat (List[str], opcional): Lista de columnas a convertir a category.
        inplace (bool): Si True, modifica el df original; si False, retorna una copia.
        call_analisis (bool): Si True, llama a analisis_exploratorio para reporting.
    Retorna:
        Dict: Diccionario con resultados y DataFrame procesado.
    """
    resultados = {}  # Diccionario para almacenar resultados
    df_out = df if inplace else df.copy()  # Decide si trabajar sobre copia o el original dependiendo de inplace
    
    # Si se especifican columnas para convertir a category
    if posibles_cat:
        df_out = forzar_a_categoria(df_out, posibles_cat, inplace=True)
        resultados['converted_to_category'] = posibles_cat

    # Si se solicita, llama a analisis_exploratorio para reporting
    if call_analisis:
        try:
            from src.analisis_exploratorio import analisis_exploratorio
            resultados['analisis'] = analisis_exploratorio(df_out)
        except Exception as e:
            resultados['analisis_error'] = str(e)

    resultados['df'] = df_out  # Añade el DataFrame procesado al resultado
    return resultados


# Demo rápida para pruebas desde terminal
if __name__ == "__main__":
    # Crea un DataFrame de ejemplo
    df_demo = pd.DataFrame({
        'A': ['x','y','x', None, 'z'],
        'B': [1,2,None,4,5],
        'C': ['alpha','beta','alpha','beta','alpha']
    })
    # Ejecuta run_checks con conversión a category y análisis exploratorio
    res = ejecutar_chequeos(df_demo, posibles_cat=['A','C'], call_analisis=True)
    print("\nColumnas convertidas:", res.get('converted_to_category', []))

def limpiar_nombres_columnas(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Normaliza los nombres de columnas de un DataFrame al formato snake_case (PEP 8), asegurando consistencia y compatibilidad.
    
    Detalle de pasos realizados:
        1. Elimina espacios en blanco al inicio y final.
        2. Reemplaza espacios internos por guiones bajos (_).
        3. Reemplaza puntos (.) por guiones bajos (_).
        4. Convierte todo a minúsculas.
        5. Elimina caracteres no alfanuméricos (excepto guiones bajos).
        6. Elimina guiones bajos duplicados o innecesarios.
    
    Args:
        df (pd.DataFrame): DataFrame original.
        verbose (bool): Si es True, imprime los cambios realizados.
        
    Returns:
        pd.DataFrame: Copia del DataFrame con nombres de columnas normalizados.
        
    Ejemplo:
        >>> df_original = pd.DataFrame(columns=['ID', 'cons.price.idx', 'Dt_Customer', 'KidHome_'])
        >>> df_clean = limpiar_nombres_columnas(df_original)
        ID → id
        cons.price.idx → cons_price_idx
        Dt_Customer → dt_customer
        KidHome_ → kidhome
    """
    df_normalizado = df.copy()
    mapeo = {}  # Diccionario para almacenar el mapeo de nombres originales a normalizados
    for col in df.columns:
        # 1. Convierte el nombre a minúsculas para uniformidad
        nuevo_nombre = col.lower()
        # 2. Reemplaza puntos, espacios y guiones por guiones bajos
        nuevo_nombre = nuevo_nombre.replace('.', '_')
        nuevo_nombre = nuevo_nombre.replace(' ', '_')
        nuevo_nombre = nuevo_nombre.replace('-', '_')
        # 3. Elimina caracteres especiales (solo deja letras minúsculas, números y _)
        nuevo_nombre = re.sub(r'[^a-z0-9_]', '', nuevo_nombre)
        # 4. Sustituye múltiples guiones bajos consecutivos por uno solo
        nuevo_nombre = re.sub(r'_+', '_', nuevo_nombre)
        # 5. Elimina guiones bajos al inicio o final del nombre
        nuevo_nombre = nuevo_nombre.strip('_')
        # Guarda el mapeo de nombre original a normalizado
        mapeo[col] = nuevo_nombre
    # Renombra las columnas usando el mapeo generado
    df_normalizado = df.rename(columns=mapeo)
    # Si verbose=True, imprime los cambios realizados o indica si ya cumplían el estándar
    if verbose:
        print("\n--- Normalización de Nombres de Columnas ---")
        cambios = [(old, new) for old, new in mapeo.items() if old != new]
        if cambios:
            for old, new in cambios:
                print(f"  {old} → {new}")
        else:
            print("  ✓ Todas las columnas ya cumplían el estándar snake_case")
    return df_normalizado
    # df_limpio = clean_column_names(df_original)