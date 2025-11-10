# Módulo: data_cleaning.py

Herramientas para la limpieza y transformación de DataFrames en proyectos de Ciencia de Datos.

Este módulo está diseñado para:

- Realizar transformaciones de tipos de datos (coerciones a category).
- Imputar valores faltantes usando diferentes estrategias (mediana, moda).
- Proporcionar un wrapper (run_checks) que combina transformaciones y puede delegar
  el reporting a analisis_exploratorio.py.

---

## FUNCIONES DISPONIBLES EN ESTE MÓDULO:

1. coerce_to_category(df, columns, inplace=False)

   - Convierte columnas especificadas al tipo category.
   - Argumentos:
     df: DataFrame a modificar.
     columns: Lista de columnas a convertir.
     inplace: Si True, modifica el df original.
   - Retorna: DataFrame con conversiones aplicadas.

2. impute_median(df, columns, inplace=False)

   - Imputa la mediana en columnas numéricas especificadas.
   - Argumentos:
     df: DataFrame a modificar.
     columns: Lista de columnas para imputar.
     inplace: Si True, modifica el df original.
   - Retorna: DataFrame con imputaciones aplicadas.

3. impute_mode(df, columns, inplace=False)

   - Imputa la moda en columnas especificadas.
   - Argumentos:
     df: DataFrame a modificar.
     columns: Lista de columnas para imputar.
     inplace: Si True, modifica el df original.
   - Retorna: DataFrame con imputaciones aplicadas.

4. run_checks(df, posibles_cat=None, inplace=False, call_analisis=False)
   - Wrapper que combina transformaciones y puede llamar a analisis_exploratorio.
   - Argumentos:
     df: DataFrame a procesar.
     posibles_cat: Lista de columnas a convertir a category.
     inplace: Si True, modifica el df original.
     call_analisis: Si True, llama a analisis_exploratorio para reporting.
   - Retorna: Dict con resultados y DataFrame procesado.

---

## BUENAS PRÁCTICAS/TIPS:

- Este módulo se centra en transformaciones (NO en reporting).
- Para análisis exploratorio y visualización, usar src.analisis_exploratorio y src.plotting.
- Las funciones son puras: si inplace=False, retornan nuevo DataFrame sin modificar el original.
- Preferir call_analisis=True en run_checks() si necesitas tanto transformación como reporting.

---

## EJEMPLO DE USO EN NOTEBOOK:

import src.data_cleaning as dc

# Solo transformación

df_clean = dc.coerce_to_category(df, ['education', 'marital'])
df_clean = dc.impute_median(df_clean, ['age', 'balance'])

# Transformación + reporting

results = dc.run_checks(df,
posibles_cat=['education', 'marital'],
call_analisis=True)
df_processed = results['df']
