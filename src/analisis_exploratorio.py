
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
from typing import List, Dict, Union, Any  # Tipado estático
import src.plotting as pl  # Importar módulo de gráficos para funciones de alto nivel

# Lista de funciones exportadas por el módulo
__all__ = [
     "analisis_exploratorio",
     "reportar_estructura",
     "obtener_columnas_categoricas",
     "resumen_categoricas",
     "hay_outliers",
     "porcentaje_outliers",
     "analizar_variables_numericas",
     "analizar_variables_categoricas",
     "analizar_tendencias_temporales",
     "analizar_variables_macro",
     "analizar_factores_campana",
     "generar_reporte_ejecutivo"
]



def reportar_estructura(df: pd.DataFrame, show_head: int = 5) -> Dict:
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


def obtener_columnas_categoricas(df: pd.DataFrame) -> List[str]:
    """
    Devuelve lista de columnas categóricas (object o category).
    Parámetros:
        df (pd.DataFrame): DataFrame a analizar.
    Retorna:
        List[str]: lista de nombres de columnas categóricas.
    """
    # Selecciona columnas de tipo object o category
    return df.select_dtypes(include=['object', 'category']).columns.tolist()


def resumen_categoricas(df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
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
    cat_cols = obtener_columnas_categoricas(df)  # Obtiene columnas categóricas
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

    resultados: Dict[str, Any] = {}  # Diccionario para almacenar resultados
    # 1. Estructura básica
    resultados['structure'] = reportar_estructura(df, mostrar_head)

    # 2. Variables categóricas
    cat_cols = obtener_columnas_categoricas(df)
    resultados['categorical_columns'] = cat_cols
    if cat_cols:
        print("\n2) VARIABLES CATEGÓRICAS")
        print("-" * 40)
        print("Columnas categóricas:", cat_cols)
        resultados['categorical_summary'] = resumen_categoricas(df, top_n=3)
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


def hay_outliers(serie):
    """
    Detecta si existen outliers en una serie numérica usando el criterio del rango intercuartílico (IQR).

    Un valor se considera outlier si está por debajo de Q1 - 1.5*IQR o por encima de Q3 + 1.5*IQR,
    donde Q1 es el primer cuartil (percentil 25), Q3 es el tercer cuartil (percentil 75) e IQR = Q3 - Q1.

    Parámetros:
        serie (pd.Series): Serie numérica sobre la que se desea detectar outliers.

    Retorna:
        bool: True si existe al menos un outlier en la serie, False si no hay outliers.

    Ejemplo:
        >>> import pandas as pd
        >>> s = pd.Series([1, 2, 2, 3, 4, 100])
        >>> hay_outliers(s)
        True
    """
    q1 = serie.quantile(0.25)  # Primer cuartil (25%)
    q3 = serie.quantile(0.75)  # Tercer cuartil (75%)
    iqr = q3 - q1  # Rango intercuartílico (IQR)
    lower = q1 - 1.5 * iqr  # Límite inferior para considerar outlier
    upper = q3 + 1.5 * iqr  # Límite superior para considerar outlier
    # Devuelve True si existe al menos un valor fuera de los límites definidos
    return ((serie < lower) | (serie > upper)).any()


def porcentaje_outliers(serie):
    """
    Calcula el porcentaje de outliers en una serie numérica usando el criterio del rango intercuartílico (IQR).

    Un valor se considera outlier si está por debajo de Q1 - 1.5*IQR o por encima de Q3 + 1.5*IQR,
    donde Q1 es el primer cuartil (percentil 25), Q3 es el tercer cuartil (percentil 75) e IQR = Q3 - Q1.

    Parámetros:
        serie (pd.Series): Serie numérica sobre la que se desea calcular el porcentaje de outliers.

    Retorna:
        float: Porcentaje de valores considerados outliers respecto al total de la serie.

    Ejemplo:
        >>> import pandas as pd
        >>> s = pd.Series([1, 2, 2, 3, 4, 100])
        >>> porcentaje_outliers(s)
        16.666666666666668
    """
    q1 = serie.quantile(0.25)  # Primer cuartil
    q3 = serie.quantile(0.75)  # Tercer cuartil
    iqr = q3 - q1  # Rango intercuartílico
    lower = q1 - 1.5 * iqr  # Límite inferior
    upper = q3 + 1.5 * iqr  # Límite superior
    return 100 * ((serie < lower) | (serie > upper)).sum() / len(serie)  # % de outliers respecto al total


def analizar_variables_numericas(
    df: pd.DataFrame,
    target_col: str,
    variables: List[str],
    output: Any = None
) -> Dict:
    """
    Analiza múltiples variables numéricas comparando grupos por target.
    Genera estadísticas descriptivas y gráficos comparativos.
    """
    resultados = {}
    print(f"\n--- ANÁLISIS DE VARIABLES NUMÉRICAS ({len(variables)}) ---")
    
    for var in variables:
        if var not in df.columns:
            continue
            
        print(f"\nAnalizando: {var}")
        # Estadísticas por grupo
        stats = df.groupby(target_col)[var].describe()
        if output:
            output.print(f"\nEstadísticas para {var}:")
            output.print(stats)
        else:
            display(stats)
            
        # Detección de outliers
        pct_outliers = porcentaje_outliers(df[var])
        print(f"Porcentaje de outliers: {pct_outliers:.2f}%")
        
        resultados[var] = {
            'stats': stats,
            'outliers_pct': pct_outliers
        }
        
    # Generar gráficos comparativos
    print("\nGenerando gráficos comparativos...")
    nombres_graficos = {var: f'num_comp_{var}_vs_{target_col}.png' for var in variables}
    colores = {var: ['skyblue', 'orange'] for var in variables}
    
    pl.graficar_comparacion_numerica(
        df, variables, target_col, nombres_graficos, colores, figsize=(12, 4)
    )
    
    return resultados


def analizar_variables_categoricas(
    df: pd.DataFrame,
    target_col: str,
    variables: List[str],
    output: Any = None
) -> Dict:
    """
    Analiza múltiples variables categóricas calculando tasas de éxito.
    Genera tablas de contingencia y gráficos de barras.
    """
    resultados = {}
    print(f"\n--- ANÁLISIS DE VARIABLES CATEGÓRICAS ({len(variables)}) ---")
    
    for var in variables:
        if var not in df.columns:
            continue
            
        print(f"\nAnalizando: {var}")
        # Calcular tasas
        tasas = calcular_tasa_proporciones(df, var).sort_values('tasa_exito', ascending=False)
        
        if output:
            output.print(f"\nTasas de conversión para {var}:")
            output.print(tasas)
        else:
            display(tasas)
            
        # Graficar
        pl.graficar_tasa_categorica(
            df, var, target_col, 
            title=f"Tasa de Conversión por {var}",
            rotation=45 if df[var].nunique() > 5 else 0
        )
        pl.guardar_grafico(f'cat_rate_{var}.png')
        
        resultados[var] = tasas
        
    return resultados


def analizar_tendencias_temporales(
    df: pd.DataFrame,
    target_col: str,
    columnas_temporales: List[str],
    output: Any = None
) -> Dict:
    """
    Analiza patrones temporales (mes, año, fecha completa).
    """
    resultados = {}
    print(f"\n--- ANÁLISIS DE TENDENCIAS TEMPORALES ---")
    
    for col in columnas_temporales:
        if col not in df.columns:
            continue
            
        print(f"\nAnalizando tendencia por: {col}")
        # Calcular métricas agrupadas
        tendencia = df.groupby(col)[target_col].agg(['count', 'mean'])
        tendencia['mean'] = tendencia['mean'] * 100
        tendencia.columns = ['Volumen', 'Tasa (%)']
        
        if output:
            output.print(f"\nTendencia por {col}:")
            output.print(tendencia)
        else:
            display(tendencia)
            
        # Graficar usando la nueva función de plotting
        pl.graficar_tendencias_temporales(
            df, col, target_col, f'tendencia_{col}.png'
        )
        resultados[col] = tendencia
        
    return resultados


def analizar_variables_macro(
    df: pd.DataFrame,
    target_col: str,
    variables_macro: List[str],
    output: Any = None
) -> Dict:
    """
    Analiza variables macroeconómicas agrupadándolas por cuartiles 
    para identificar correlaciones no lineales con el target.
    """
    resultados = {}
    print(f"\n--- ANÁLISIS MACROECONÓMICO ---")
    
    for var in variables_macro:
        if var not in df.columns:
            continue
            
        print(f"\nAnalizando impacto macro: {var}")
        
        # Crear cuartiles para análisis discretizado
        try:
            df[f'{var}_cuartil'] = pd.qcut(df[var], q=4, duplicates='drop')
            tasas_q = calcular_tasa_proporciones(df, f'{var}_cuartil')
            
            if output:
                output.print(f"\nAnálisis por cuartiles de {var}:")
                output.print(tasas_q)
            else:
                display(tasas_q)
                
            resultados[var] = tasas_q
            
            # Graficar relación
            pl.graficar_boxplot_por_target(df, var, target_col)
            pl.guardar_grafico(f'macro_box_{var}.png')
            
        except Exception as e:
            print(f"Error analizando {var}: {e}")
            
    return resultados


def analizar_factores_campana(
    df: pd.DataFrame,
    target_col: str,
    output: Any = None
) -> Dict:
    """
    Analiza factores específicos de campaña directa (duration, poutcome, previous, campaign).
    """
    columnas_clave = ['duration', 'campaign', 'pdays', 'previous', 'poutcome']
    print(f"\n--- ANÁLISIS DE FACTORES DE CAMPAÑA ---")
    
    # Reutiliza las funciones genéricas para las variables correspondientes
    vars_num = [c for c in columnas_clave if c in df.select_dtypes(include=np.number).columns]
    vars_cat = [c for c in columnas_clave if c in df.select_dtypes(include=['object', 'category']).columns]
    
    res_num = analizar_variables_numericas(df, target_col, vars_num, output)
    res_cat = analizar_variables_categoricas(df, target_col, vars_cat, output)
    
    return {**res_num, **res_cat}


def generar_reporte_ejecutivo(
    tasas_por_variable: Dict,
    output: Any
) -> None:
    """
    Genera un resumen ejecutivo consolidado del análisis EDA.
    
    Consolida los hallazgos de todas las secciones del análisis exploratorio:
    - Análisis temporal (patrones estacionales)
    - Variables numéricas (diferencias entre grupos)
    - Variables categóricas (tasas de conversión)
    - Variables macroeconómicas (correlaciones)
    - Factores de campaña (duración y resultado anterior)
    - Resumen general (conteo de variables analizadas)
    
    Args:
        tasas_por_variable: Diccionario con resultados de todos los análisis realizados
        output: Objeto DualOutput para escribir el reporte
    
    Returns:
        None (escribe directamente en el objeto output)
    
    Ejemplo:
        >>> output = DualOutput('../reports/outputs/analisis_EDA_completo.txt')
        >>> # ... ejecutar análisis y poblar tasas_por_variable ...
        >>> generar_reporte_ejecutivo(tasas_por_variable, output)
        >>> output.save()
    """
    if not output:
        return
    
    # Importar datetime para timestamp
    from datetime import datetime
    
    # =========================================================================
    # ENCABEZADO DEL REPORTE
    # =========================================================================
    output.print("\n" + "="*80)
    output.print("RESUMEN EJECUTIVO: ANÁLISIS EXPLORATORIO DE DATOS (EDA)")
    output.print("="*80)
    output.print(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.print("="*80)
    
    # =========================================================================
    # SECCIÓN 1: ANÁLISIS TEMPORAL
    # =========================================================================
    output.print("\n📅 ANÁLISIS TEMPORAL - Patrones estacionales:")
    
    # Análisis por mes (variable date)
    if 'temporal_mes' in tasas_por_variable:
        data = tasas_por_variable['temporal_mes']
        if 'tasa_exito_por_mes' in data and 'registros_por_mes' in data:
            tasas_mes = pd.Series(data['tasa_exito_por_mes'])
            registros_mes = pd.Series(data['registros_por_mes'])
            mes_max_tasa = tasas_mes.idxmax()
            mes_min_tasa = tasas_mes.idxmin()
            output.print(f"\n  DISTRIBUCIÓN POR MES (date):")
            output.print(f"    Mayor tasa: {mes_max_tasa} → {tasas_mes[mes_max_tasa]:.1%} ({registros_mes[mes_max_tasa]:.0f} registros)")
            output.print(f"    Menor tasa: {mes_min_tasa} → {tasas_mes[mes_min_tasa]:.1%} ({registros_mes[mes_min_tasa]:.0f} registros)")
    
    # Análisis por mes de contacto (contact_month)
    if 'temporal_contact_month' in tasas_por_variable:
        data = tasas_por_variable['temporal_contact_month']
        if 'tasa_exito' in data and 'registros' in data:
            tasas_mes_contact = pd.Series(data['tasa_exito'])
            registros_mes_contact = pd.Series(data['registros'])
            mes_max_contact = tasas_mes_contact.idxmax()
            mes_min_contact = tasas_mes_contact.idxmin()
            output.print(f"\n  MES DE CONTACTO (contact_month):")
            output.print(f"    Mayor tasa: {mes_max_contact} → {tasas_mes_contact[mes_max_contact]:.1%} ({registros_mes_contact[mes_max_contact]:.0f} registros)")
            output.print(f"    Menor tasa: {mes_min_contact} → {tasas_mes_contact[mes_min_contact]:.1%} ({registros_mes_contact[mes_min_contact]:.0f} registros)")
    
    # Análisis por año de contacto
    if 'temporal_contact_year' in tasas_por_variable:
        data = tasas_por_variable['temporal_contact_year']
        if 'tasa_exito_por_anio' in data and 'registros_por_anio' in data:
            tasas_anio = pd.Series(data['tasa_exito_por_anio'])
            registros_anio = pd.Series(data['registros_por_anio'])
            output.print(f"\n  AÑO DE CONTACTO (contact_year):")
            for anio in sorted(tasas_anio.index):
                output.print(f"   {int(anio)}: {tasas_anio[anio]:.1%} ({registros_anio[anio]:.0f} registros)")
    
    # =========================================================================
    # SECCIÓN 2: VARIABLES NUMÉRICAS
    # =========================================================================
    output.print("\n📊 VARIABLES NUMÉRICAS - Diferencias entre grupos (y=1 vs y=0):")
    for var in ['age', 'income', 'tenure_years']:
        if var in tasas_por_variable and 'comparativa' in tasas_por_variable[var]:
            comp = tasas_por_variable[var]['comparativa']
            if comp['ratio'] is not None:
                output.print(f"  • {tasas_por_variable[var]['config']['titulo']}: {comp['ratio']:.2f}x (y=1/y=0)")
    
    # =========================================================================
    # SECCIÓN 3: VARIABLES CATEGÓRICAS
    # =========================================================================
    output.print("\n📊 VARIABLES CATEGÓRICAS - Tasas de conversión destacadas:")
    for var in ['job', 'marital', 'age_group', 'education']:
        if var in tasas_por_variable and 'tabla' in tasas_por_variable[var]:
            tabla_dict = tasas_por_variable[var]['tabla']
            if tabla_dict and 'tasa_exito' in tabla_dict:
                titulo = tasas_por_variable[var]['config']['titulo']
                # Reconstruir DataFrame desde el dict
                df_tasas = pd.DataFrame(tabla_dict)
                if not df_tasas.empty and 'tasa_exito' in df_tasas.columns:
                    df_tasas = df_tasas.sort_values('tasa_exito', ascending=False)
                    top_idx = df_tasas.index[0]
                    bot_idx = df_tasas.index[-1]
                    top_tasa = df_tasas['tasa_exito'].iloc[0]
                    bot_tasa = df_tasas['tasa_exito'].iloc[-1]
                    output.print(f"\n  {titulo.upper()}:")
                    output.print(f"    Mayor: {top_idx} → {top_tasa:.1%}")
                    output.print(f"    Menor: {bot_idx} → {bot_tasa:.1%}")
    
    # =========================================================================
    # SECCIÓN 4: VARIABLES MACROECONÓMICAS
    # =========================================================================
    output.print("\n🌍 VARIABLES MACROECONÓMICAS - Correlaciones con conversión:")
    
    # Iterar sobre las 4 variables macro almacenadas con prefijo 'macro_'
    variables_macro_orden = ['macro_emp_var_rate', 'macro_euribor3m', 'macro_cons_price_idx', 'macro_nr_employed']
    for macro_key in variables_macro_orden:
        if macro_key in tasas_por_variable:
            # Extraer el nombre original de la variable (sin el prefijo 'macro_')
            var_name = macro_key.replace('macro_', '')
            correlacion = tasas_por_variable[macro_key].get('correlacion')
            if correlacion is not None:
                output.print(f"  • {var_name}: Corr = {correlacion:.3f}")
    
    # =========================================================================
    # SECCIÓN 5: FACTORES DE CAMPAÑA
    # =========================================================================
    output.print("\n📞 FACTORES DE CAMPAÑA - Duración y resultado anterior:")
    
    # Duración de llamada
    if 'duration' in tasas_por_variable:
        comp = tasas_por_variable['duration']['comparativa']
        if comp['ratio'] is not None:
            output.print(f"\n  DURACIÓN DE LLAMADA:")
            output.print(f"    Ratio (y=1/y=0): {comp['ratio']:.2f}x")
            output.print(f"    {comp['interpretacion']}")
    
    # Resultado anterior (poutcome)
    if 'poutcome' in tasas_por_variable:
        tabla_dict = tasas_por_variable['poutcome']['tabla']
        df_pout = pd.DataFrame(tabla_dict)
        if not df_pout.empty and 'tasa_exito' in df_pout.columns:
            df_pout = df_pout.sort_values('tasa_exito', ascending=False)
            output.print(f"\n  RESULTADO ANTERIOR (poutcome):")
            for idx in df_pout.index:
                tasa = df_pout.loc[idx, 'tasa_exito']
                n = df_pout.loc[idx, 'n']
                output.print(f"    {idx}: {tasa:.1%} (n={n:.0f})")
    
    # =========================================================================
    # SECCIÓN 6: RESUMEN GENERAL
    # =========================================================================
    output.print("\n" + "="*80)
    output.print("HALLAZGOS CLAVE:")
    output.print(f"  • Total de variables analizadas: {len(tasas_por_variable)}")
    
    # Contar tipos de análisis
    n_temporal = sum(1 for k in tasas_por_variable.keys() if 'temporal' in k)
    n_numericas = sum(1 for k in ['age', 'income', 'tenure_years'] if k in tasas_por_variable)
    n_categoricas = sum(1 for k in ['job', 'marital', 'age_group', 'education'] if k in tasas_por_variable)
    n_macro = sum(1 for k in tasas_por_variable.keys() if k.startswith('macro_'))
    n_campana = sum(1 for k in ['duration', 'poutcome'] if k in tasas_por_variable)
    
    output.print(f"  • Variables temporales: {n_temporal}")
    output.print(f"  • Variables numéricas: {n_numericas}")
    output.print(f"  • Variables categóricas: {n_categoricas}")
    output.print(f"  • Variables macroeconómicas: {n_macro}")
    output.print(f"  • Factores de campaña: {n_campana}")
    output.print("="*80)

