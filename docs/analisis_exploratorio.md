# Módulo: analisis_exploratorio.py

Herramientas para el análisis exploratorio sistemático de DataFrames en proyectos de Ciencia de Datos.

Este módulo está diseñado para:

- Realizar un análisis exploratorio inicial de cualquier DataFrame, clasificando y resumiendo las variables presentes.
- Diferenciar y analizar tanto variables categóricas como numéricas.
- Reportar valores faltantes de manera estructurada.
- Visualizar información clave de los datos de manera reproducible y automática, ideal para notebooks o scripts.
- Ofrecer un flujo rápido y seguro para obtener diagnósticos esenciales antes de limpiar o modelar los datos.

---

## FUNCIONES DISPONIBLES EN ESTE MÓDULO:

1. report_structure(df, show_head=5)

   - Imprime y devuelve información básica del DataFrame: dimensiones, tipos de datos y primeras filas.
   - Argumentos:
     df: DataFrame a analizar.
     show_head (int): filas de ejemplo a mostrar.
   - Retorna: dict con 'shape', 'dtypes' y 'head'.

2. get_categorical_columns(df)

   - Devuelve una lista con los nombres de las columnas categóricas (object o category).

3. categorical_summary(df, top_n=3)

   - Devuelve un DataFrame resumen con número de valores únicos y los top N valores y sus cuentas
     para cada columna categórica detectada en el DataFrame.

4. analisis_exploratorio(df, nombre_df="DataFrame", mostrar_head=5, round_decimals=2)
   - Función principal que organiza y muestra:
     - Estructura básica (report_structure)
     - Resumen de variables categóricas (categorical_summary)
     - Resumen de variables numéricas (describe)
     - Tabla de valores faltantes con porcentajes
   - Retorna un dict con los resultados intermedios (estructura, listas de columnas, missing, etc.).

---

## BUENAS PRÁCTICAS/TIPS:

- Llama a analisis_exploratorio(df) tras cargar un DataFrame para una inspección rápida.
- Este módulo se centra en reporting; NO debe mutar el DataFrame de entrada.
- Para transformaciones (coerciones, imputaciones), utiliza src.data_cleaning, para utiliza visualizaciones src.plotting.

---

## EJEMPLO DE USO EN NOTEBOOK:

from src.analisis_exploratorio import analisis_exploratorio
analisis_exploratorio(df_mis_datos, nombre_df="Datos de Clientes")
