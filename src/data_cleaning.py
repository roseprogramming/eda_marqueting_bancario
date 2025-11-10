"""
Módulo: data_cleaning.py
======================================================

Herramientas para la limpieza y transformación de DataFrames en proyectos de Ciencia de Datos.

Este módulo está diseñado para:
- Realizar transformaciones de tipos de datos (coerciones a category).
- Imputar valores faltantes usando diferentes estrategias (mediana, moda).
- Proporcionar un wrapper (run_checks) que combina transformaciones y puede delegar 
  el reporting a analisis_exploratorio.py.

------------------------------------------------------
FUNCIONES DISPONIBLES EN ESTE MÓDULO:
------------------------------------------------------

1) coerce_to_category(df, columns, inplace=False)
   - Convierte columnas especificadas al tipo category.
   - Argumentos:
       df: DataFrame a modificar.
       columns: Lista de columnas a convertir.
       inplace: Si True, modifica el df original.
   - Retorna: DataFrame con conversiones aplicadas.

2) impute_median(df, columns, inplace=False)
   - Imputa la mediana en columnas numéricas especificadas.
   - Argumentos:
       df: DataFrame a modificar.
       columns: Lista de columnas para imputar.
       inplace: Si True, modifica el df original.
   - Retorna: DataFrame con imputaciones aplicadas.

3) impute_mode(df, columns, inplace=False)
   - Imputa la moda en columnas especificadas.
   - Argumentos:
       df: DataFrame a modificar.
       columns: Lista de columnas para imputar.
       inplace: Si True, modifica el df original.
   - Retorna: DataFrame con imputaciones aplicadas.

4) run_checks(df, posibles_cat=None, inplace=False, call_analisis=False)
   - Wrapper que combina transformaciones y puede llamar a analisis_exploratorio.
   - Argumentos:
       df: DataFrame a procesar.
       posibles_cat: Lista de columnas a convertir a category.
       inplace: Si True, modifica el df original.
       call_analisis: Si True, llama a analisis_exploratorio para reporting.
   - Retorna: Dict con resultados y DataFrame procesado.

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
results = dc.run_checks(df, 
                       posibles_cat=['education', 'marital'],
                       call_analisis=True)
df_processed = results['df']
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Union, Optional

__all__ = [
    "coerce_to_category",
    "impute_median", 
    "impute_mode",
    "run_checks"
]

def coerce_to_category(df: pd.DataFrame, columns: List[str], inplace: bool = False) -> pd.DataFrame:
    """Convierte columnas especificadas al tipo category."""
    if not inplace:
        df = df.copy()
    for c in columns or []:
        if c in df.columns:
            df[c] = df[c].astype('category')
    return df

def impute_median(df: pd.DataFrame, columns: List[str], inplace: bool = False) -> pd.DataFrame:
    """Imputa la mediana en columnas numéricas especificadas."""
    if not inplace:
        df = df.copy()
    for c in columns or []:
        if c in df.columns and pd.api.types.is_numeric_dtype(df[c]):
            df[c] = df[c].fillna(df[c].median())
    return df

def impute_mode(df: pd.DataFrame, columns: List[str], inplace: bool = False) -> pd.DataFrame:
    """Imputa la moda en columnas especificadas."""
    if not inplace:
        df = df.copy()
    for c in columns or []:
        if c in df.columns:
            mode = df[c].mode(dropna=True)
            if not mode.empty:
                df[c] = df[c].fillna(mode.iloc[0])
    return df

def run_checks(df: pd.DataFrame, posibles_cat: Optional[List[str]] = None,
               inplace: bool = False, call_analisis: bool = False) -> Dict:
    """
    Wrapper que combina transformaciones y puede llamar a analisis_exploratorio.
    Retorna dict con resultados y DataFrame procesado.
    """
    resultados = {}
    df_out = df if inplace else df.copy()
    
    # Aplicar transformaciones si se solicitan
    if posibles_cat:
        df_out = coerce_to_category(df_out, posibles_cat, inplace=True)
        resultados['converted_to_category'] = posibles_cat

    # Opcionalmente llamar a analisis_exploratorio para reporting
    if call_analisis:
        try:
            from src.analisis_exploratorio import analisis_exploratorio
            resultados['analisis'] = analisis_exploratorio(df_out)
        except Exception as e:
            resultados['analisis_error'] = str(e)

    resultados['df'] = df_out
    return resultados

if __name__ == "__main__":
    # Demo rápida
    df_demo = pd.DataFrame({
        'A': ['x','y','x', None, 'z'],
        'B': [1,2,None,4,5],
        'C': ['alpha','beta','alpha','beta','alpha']
    })
    
    # Ejemplo de uso
    res = run_checks(df_demo, 
                    posibles_cat=['A','C'],
                    call_analisis=True)
    print("\nColumnas convertidas:", res.get('converted_to_category', []))
    
def clean_column_names(df, verbose=True):
    """
    Normaliza los nombres de columnas siguiendo el estándar snake_case de PEP 8.
    
    Transformaciones aplicadas:
    - Convierte a minúsculas
    - Reemplaza puntos, espacios y guiones por guiones bajos
    - Elimina caracteres especiales al inicio/final
    - Elimina guiones bajos duplicados
    - Elimina guiones bajos al inicio/final
    
    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame a normalizar
    verbose : bool, default=True
        Si True, muestra el mapeo de nombres antiguos → nuevos
    
    Retorna:
    --------
    pd.DataFrame
        DataFrame con columnas normalizadas
    
    Ejemplo:
    --------
    >>> df.columns = ['ID', 'cons.price.idx', 'Dt_Customer', 'KidHome_']
    >>> df_clean = normalizar_nombres_columnas(df)
    ID → id
    cons.price.idx → cons_price_idx
    Dt_Customer → dt_customer
    KidHome_ → kidhome
    """
    import re
    
    # Diccionario para almacenar el mapeo
    mapeo = {}
    
    for col in df.columns:
        # 1. Convertir a minúsculas
        nuevo_nombre = col.lower()
        
        # 2. Reemplazar puntos, espacios, guiones por guiones bajos
        nuevo_nombre = nuevo_nombre.replace('.', '_')
        nuevo_nombre = nuevo_nombre.replace(' ', '_')
        nuevo_nombre = nuevo_nombre.replace('-', '_')
        
        # 3. Eliminar caracteres especiales (mantener solo letras, números y _)
        nuevo_nombre = re.sub(r'[^a-z0-9_]', '', nuevo_nombre)
        
        # 4. Eliminar guiones bajos duplicados
        nuevo_nombre = re.sub(r'_+', '_', nuevo_nombre)
        
        # 5. Eliminar guiones bajos al inicio/final
        nuevo_nombre = nuevo_nombre.strip('_')
        
        mapeo[col] = nuevo_nombre
    
    # Renombrar columnas
    df_normalizado = df.rename(columns=mapeo)
    
    # Mostrar cambios si verbose=True
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