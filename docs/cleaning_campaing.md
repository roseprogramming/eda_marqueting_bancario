# Módulo: cleaning_campaign.py

Módulo principal para la limpieza, transformación y preparación del DataFrame de campañas bancarias (`df_campaign`) para las etapas de análisis y modelado.

Este módulo está diseñado para:

- **Limpieza y transformación estructurada** del DataFrame según especificaciones del proyecto (tipos, valores especiales, formato de fechas y variables categóricas).
- **Normalización Temporal**: Extrae, limpia y tipa correctamente fechas, meses y años para análisis longitudinal y de estacionalidad.
- **Corrección de Tipos Numéricos**: Corrige objetos mal tipados (ej. valores macroeconómicos) debido a separadores decimales incorrectos (comas).
- **Gestión de Valores Especiales**: Recodifica marcadores como `999` en `pdays` y el target binario `y` (`yes`/`no` → `1`/`0`).
- **Imputación de Valores Faltantes**: Aplica estrategias de imputación (mediana para numéricas, moda para categóricas) a columnas críticas.
- **Asegurar Calidad**: Prepara un DataFrame estructuralmente correcto y listo para ser consumido por módulos de visualización y _machine learning_.

---

## FUNCIONES DISPONIBLES EN ESTE MÓDULO:

1. clean_campaign_df(df_campaign_original)
   - Función principal que aplica la secuencia completa de limpieza y transformación del DataFrame de la campaña bancaria.
   - Pasos incluidos: corrección de separadores, conversión a `datetime`, recodificación de `pdays` y target `y`, imputación y tipado categórico.
   - Argumentos:
     df_campaign_original (pd.DataFrame): DataFrame original (sin modificar) con los datos de la campaña.
   - Retorna: pd.DataFrame limpio y listo para análisis/modelado.

---

## BUENAS PRÁCTICAS/TIPS:

- **Inmutabilidad:** La lógica de la función `clean_campaign_df` debe usar una copia (`df.copy()`) del DataFrame de entrada para no mutar el original.
- **Validación:** Posterior a la limpieza, se recomienda la validación con `run_checks()` o una inspección visual para asegurar la calidad.
- **Modularidad:** Para utilidades de limpieza más genéricas y reusables (ej. manejo de NaNs), basarse en el módulo `src.data_cleaning`.

---

## EJEMPLO DE USO EN NOTEBOOK:

import cleaning_campaign as cc
import pandas as pd

# Suponiendo que df_campaign ya está cargado

df_campaign_clean = cc.clean_campaign_df(df_campaign)

print(df_campaign_clean.head())

"""
Módulo: cleaning_campaign.py
======================================================
Módulo principal para la limpieza, transformación y preparación del DataFrame de campañas bancarias (`df_campaign`) para las etapas de análisis y modelado.

---

Este módulo está diseñado para:

- **Limpieza y transformación estructurada** del DataFrame según especificaciones del proyecto (tipos, valores especiales, formato de fechas y variables categóricas).
- **Normalización Temporal**: Extrae, limpia y tipa correctamente fechas, meses y años para análisis longitudinal y de estacionalidad.
- **Corrección de Tipos Numéricos**: Corrige objetos mal tipados (ej. valores macroeconómicos) debido a separadores decimales incorrectos (comas).

---

## RESUMEN DE LA RESOLUCIÓN DE PROBLEMAS DE TIPOS (DTYPE FIX)

La versión actual del script resuelve tres problemas principales de tipos de datos: age (float a int), variables macroeconómicas (object a float) y reversión de tipos por módulos externos.

1.  CAUSA PRINCIPAL (age): IntCastingNaNError

    - **Problema:** El fallo ocurría porque la imputación de 'age' con `df.fillna(df['age'].mode())` no rellenaba correctamente todos los valores nulos (`NaN`), dejando la columna como tipo flotante con `NaN`s. Pandas prohíbe convertir `NaN` directamente a un tipo entero (`int`).
    - **Solución:** Se cambió la imputación para usar el **valor escalar de la mediana** (`df['age'].median()`) y se garantizó la conversión a **`int`** solo después de verificar que no quedaran nulos.

2.  CAUSA SECUNDARIA (Float/Object): Variables Macroeconómicas

    - **Problema:** Columnas como `euribor3m` o `cons.price.idx` se convertían a `float` en el Paso 1, pero las llamadas posteriores a funciones externas (como `dc.impute_median`) causaban que el tipo se revirtiera o se corrompiera a `object`.
    - **Solución:** Se eliminó la dependencia de `dc.impute_median` para los flotantes. La limpieza de comas, la conversión a **`float`** y la imputación con la mediana se realizan **manualmente y conjuntamente en el Paso 1** para asegurar el tipo `float` desde el inicio.

3.  CAUSA ADICIONAL: Conflicto con Módulos Externos
    _ **Problema:** La reasignación del DataFrame (`df = dc.impute_mode(df, ...)`) revertía los tipos de columnas ya limpiadas (`age`, `default`, `housing`, `loan`).
    _ **Solución:** Se implementó una **estrategia de aislamiento**:
    a. La conversión a **`int`** de `'age'` se realiza inmediatamente después de su imputación manual.
    b. Las conversiones finales a **`int`** de las columnas binarias (`default`, `housing`, `loan`) se mueven al **Paso 5**, justo antes de la conversión a `category`, para ser el último proceso que define su tipo antes de ser categorizadas.
    """
