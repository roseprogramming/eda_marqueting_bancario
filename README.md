# 📊 EDA Marketing Bancario

Análisis Exploratorio de Datos (EDA) sobre campañas de marketing bancario para identificar patrones que influyen en la suscripción de depósitos a plazo.

**Máster Data & Analytics – Módulo: Python for Data**

---

## 📚 Contexto del Proyecto

Este proyecto forma parte de la **entrega evaluable del Máster Data & Analytics** impartido por **The Power Business School**. Se desarrolló como aplicación práctica de los conocimientos adquiridos en los módulos de **Python** y **Python for Data**, demostrando competencias en:

- ✅ **Transformación y limpieza de datos** (manejo de valores faltantes, corrección de tipos, normalización)
- ✅ **Estructuras de datos avanzadas** (listas, diccionarios, funciones modulares, manejo de archivos)
- ✅ **Análisis descriptivo** (estadísticas, correlaciones, segmentación, tasas de conversión)
- ✅ **Visualización efectiva** (matplotlib, seaborn: histogramas, heatmaps, boxplots)
- ✅ **Operaciones pandas** (merge, groupby, agregaciones, creación de variables derivadas)
- ✅ **Código optimizado** (buenas prácticas, modularidad, documentación, reutilización)
- ✅ **Informe explicativo** (justificaciones basadas en datos, conclusiones fundamentadas)
- ✅ **Documentación completa** (README, informes técnicos, notebooks ejecutables)

**Dataset:** Campañas de marketing directo de un banco portugués (2012-2014), con 43,000 registros que incluyen variables demográficas, de contacto, macroeconómicas y resultado de suscripción a depósito a plazo.

**Resultado:** Pipeline ETL completo, análisis exploratorio exhaustivo con 12 visualizaciones, identificación de segmentos de alto valor y detección de data leakage, todo documentado en informes ejecutivos listos para decisiones de negocio.

---

## 🎯 Objetivo

Construir un dataset maestro limpio y documentado que permita:

- Detectar perfiles con mayor tasa de conversión.
- Identificar variables predictivas útiles.
- Evitar uso de variables con data leakage.
- Preparar una base sólida para futuros modelos.

---

## � Pasos Seguidos en el Proyecto

Este proyecto siguió una metodología estructurada en 5 fases:

### 1. **Carga y Exploración Inicial**

- Importación de `bank-additional.csv` (43,000 registros) y `customer-details.xlsx` (3 sheets)
- Inspección de tipos de datos, valores faltantes y estructura

### 2. **Transformación y Limpieza**

- Normalización de columnas a snake_case
- Conversión de decimales españoles (`,` → `.`) y fechas
- Imputación de valores faltantes (mediana/moda)
- Recodificación de variables binarias (yes/no → 1/0)

### 3. **Integración de Datasets**

- Unificación de 3 hojas Excel por año
- Merge por `id` con validaciones de integridad
- Generación de `df_perfil_cliente.csv` (master dataset)

### 4. **Análisis Exploratorio**

- Estadísticas descriptivas por segmento
- Cálculo de tasas de conversión
- Análisis de correlaciones
- Identificación de data leakage (`duration`)

### 5. **Visualización y Documentación**

- 12 gráficos clave (distribuciones, tasas, correlaciones, análisis temporal, efectividad de campañas)
- Informe ejecutivo con insights accionables
- Documentación técnica del código

**Detalles completos del proceso:**

- [Informe Preliminar](reports/documentacion/archive/informe_preliminar.md) — Limpieza y transformaciones
- [Informe Ejecutivo](reports/documentacion/informe_ejecutivo.md) — Análisis y hallazgos

---

## �📁 Estructura

```
EDA_Marketing_Bancario/
├── data/                # Incluido en Git (28.8 MB total)
│   ├── raw/             # bank-additional.csv, customer-details.xlsx
│   └── processed/       # df_campaign_clean.csv, df_customer_details.csv, df_perfil_cliente.csv
├── notebooks/
│   └── 01_EDA_Analisis.ipynb  # Notebook principal (estructura en 3 bloques)
├── src/
│   ├── pipeline.py                 # Pipeline ETL de 9 pasos
│   ├── analisis_exploratorio.py
│   ├── data_cleaning.py
│   ├── cleaning_campaign.py
│   ├── plotting.py                 # Funciones de visualización
│   └── reporte_pdf.py              # Generación de reporte PDF
├── reports/
│   ├── outputs/         # analisis_demografico_completo.txt
│   └── documentacion/
│       ├── informe_ejecutivo.md
│       └── archive/
│           └── informe_preliminar.md
├── docs/
│   └── especificaciones_proyecto.md
├── requirements.txt
└── README.md (Este archivo)
```

### 📓 Estructura del Notebook

El notebook `01_EDA_Analisis.ipynb` está organizado en **3 bloques principales**:

| Bloque       | Título                         | Contenido principal                                                        |
| ------------ | ------------------------------ | -------------------------------------------------------------------------- |
| **BLOQUE 1** | Importación y Configuración    | Librerías, configuración visual, paths, módulos, utilidades                |
| **BLOQUE 2** | Carga y Preparación (ETL)      | Pipeline ETL, carga y limpieza de datos, generación de datasets procesados |
| **BLOQUE 3** | Análisis Exploratorio de Datos | Estadísticas, distribuciones, tasas, correlaciones, perfil demográfico,    |
|              |                                | factores de campaña, visualizaciones y conclusiones                        |

---

## 🚀 Instalación

```bash
git clone https://github.com/roseprogramming/eda_marqueting_bancario.git
cd eda_marqueting_bancario
py -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
pip install -e .            # Instalar paquete en modo editable
```

Los datasets ya están incluidos en el repositorio.
Abrir y ejecutar: notebooks/01_EDA_Analisis.ipynb

## ⚡ Ejecutar Pipeline

Desde terminal:

```cmd
cd tu\proyecto
python src/pipeline.py --profile
```

**Eso es todo.** Genera 3 CSVs:

- `df_campaign_clean.csv` — Campaña limpia (8.6 MB)
- `df_customer_details.csv` — Clientes 2012-2014 (2.9 MB)
- `df_perfil_cliente.csv` ⭐ — **Master dataset (usa este en notebook)**

---

## 📝 Código del Pipeline

El archivo `src/pipeline.py` ejecuta un ETL de **9 pasos**:

1. Cargar raw data con `index_col=0`
2. Limpiar campaña con `clean_campaign_df()` + `clean_column_names()`
3. Guardar `df_campaign_clean.csv` (24 columnas)
4. Concatenar customers con keys por año + `reset_index(level=0)`
5. Normalizar customers con `clean_column_names()`
6. Guardar `df_customer_details.csv` (7 columnas)
7. Merge con `left_on='id', right_on='id'`
8. `set_index('id')` para UUID como índice
9. Guardar `df_perfil_cliente.csv` (43,000 × 29)

**Ver archivo:** [src/pipeline.py](src/pipeline.py)

---

## 📊 Informe del Análisis

### Estadísticas Clave

- **Dataset final:** 43,000 registros × 29 variables
- **Tasa de conversión global:** 11.3% (4,640 suscripciones)
- **Periodo:** 2012–2014 (campañas telefónicas)

### Hallazgos Principales

| Variable      | Insight                                       | Impacto     |
| ------------- | --------------------------------------------- | ----------- |
| **poutcome**  | Clientes con éxito previo: **65% conversión** | ⭐⭐⭐ Alto |
| **age**       | Segmento 56-65 años: **18.7% conversión**     | ⭐⭐⭐ Alto |
| **job**       | Students/Retired: >25% vs Blue-collar: 6.8%   | ⭐⭐ Medio  |
| **education** | Universidad: 13.7% vs Básica: 9.8%            | ⭐⭐ Medio  |
| **duration**  | Data leakage — No usar en modelos             | ⚠️ Crítico  |
| **income**    | Sin poder discriminatorio (ratio 1.02x)       | ⭐ Bajo     |

### Correlaciones Relevantes

- **poutcome ↔ y:** 0.32 (predictor válido)
- **duration ↔ y:** 0.59 (data leakage)
- **emp.var.rate ↔ euribor3m:** 0.97 (colinealidad macro)

### Recomendaciones Estratégicas

1. **Priorizar segmentos:** Edad 56-65, estudiantes, retirados, éxito previo
2. **Optimizar contactos:** Evaluar saturación (campaign) y estacionalidad (month)
3. **Excluir variables:** duration (leakage), income/kidhome (baja señal)

**📄 Análisis completo disponible en:**

- [Informe Ejecutivo](reports/documentacion/informe_ejecutivo.md) — Insights detallados + visualizaciones
- [Análisis Demográfico Completo](reports/outputs/analisis_demografico_completo.txt) — Salida textual del pipeline

---

## ⚠ Data Leakage

Variable `duration` solo conocida tras la llamada. Usar solo en análisis post-mortem, nunca en modelos predictivos previos al contacto.

---

## 📦 Variables recomendadas para modelado

```python
features = [
    'age','education','job','marital',
    'poutcome','contact','campaign','previous_contact',
    'contact_month','contact_day_of_week',
    'emp_var_rate','euribor3m','cons_price_idx',
    'antiguedad_años'
]
target = 'y'
```

Excluir: income, kidhome, teenhome, duration.

---

## � Dificultades Principales Encontradas

**Nota:** Este proyecto fue completado en **10 sesiones interrumpidas** (semanas entre ellas). Las principales dificultades fueron:

### 1. **Manejo de Datos Españoles**

- Decimales con coma (`,`) en lugar de punto (`.`)
- Fechas en formato `DD/MM/YYYY`
- Solución: Crear función `coerce_to_numeric()` con parámetro `decimal=','`

### 2. **Fusión de Múltiples Fuentes**

- CSV con 43K registros + Excel con 3 sheets (2012, 2013, 2014)
- Inconsistencias en ID entre datasets
- Solución: Validar merge con `assert df.shape[0] == original_count`

### 3. **Data Leakage (Descubierta Tardía)**

- Variable `duration` parecía buen predictor (r=0.59)
- Solo disponible DESPUÉS del contacto
- Impacto: Tuvimos que redesñar features a mitad del análisis
- Lección: **Validar disponibilidad temporal antes de análisis**

### 4. **Limpieza de Categorías Raras**

- Ocupaciones con <20 casos (nautical engineer, farmer, etc.)
- Decisión: Agrupar en "Other" vs mantener → impacta tasas de conversión
- Tiempo invertido: ~2 horas en decisión

### 5. **Problemas de Imports en Jupyter**

- Paths relativos no funcionaban desde notebook
- `ModuleNotFoundError` en `plotting.py`
- Solución: Agregar `sys.path.append()` y usar `project_root`

### 6. **Over-Engineering Inicial**

- Código con duplicidades (funciones en 3 archivos distintos)
- Arquitectura con 6+ módulos innecesarios
- Solución: Refactorizar a **5 módulos clave** solamente

### 7. **Gestión de Memoria**

- 43K × 30 variables causan lentitud en cálculos
- Heatmap de 22×22 generaba PNG de 888 KB
- Solución: Excluir variables colineales antes de visualizar

### 8. **Dependencias Faltantes**

- KDE (Kernel Density Estimate) requería scipy
- Necesitó instalar en venv + restart del kernel

### 9. **Decisiones Arquitectónicas Sin Claridad**

- ¿Guardar datos procesados en CSV o memoria?
- ¿Qué hacer con valores faltantes? (mean/median/drop)
- ¿Cuántas visualizaciones son "suficientes"?
- Solución: **Documentar decisiones en docstrings y comments**

### 10. **Bug en Limpieza de Variables Binarias**

- **Contexto:** Las columnas `default`, `housing`, `loan` contenían valores 'yes'/'no' además de '1'/'0'.
- **Problema:** La función de limpieza no contemplaba 'yes'/'no', dejándolos como '0' por defecto o causando inconsistencias.
- **Detección:** Identificado al crear *unit tests* para el módulo de limpieza.
- **Solución:** Actualizar el diccionario de reemplazo en `cleaning_campaign.py`.

### Reflexión sobre la evolución y el aprendizaje

A lo largo del desarrollo, muchas de estas dificultades surgieron a medida que tomaba decisiones sobre la arquitectura y la modularidad del proyecto. Por un lado, busqué hacer el código más modular y robusto, dividiendo funciones en varios scripts y mejorando la reutilización. Por otro, fui simplificando el archivo principal (el notebook) para que fuera más claro y fácil de seguir.

En ocasiones, al cambiar de estrategia o cuando una decisión no funcionaba como esperaba, tuve que identificar el punto exacto de error, volver atrás y restaurar partes del trabajo anterior, procurando no perder los avances y mejoras que sí me gustaban. Este proceso de prueba, error y ajuste me permitió aprender a equilibrar la complejidad técnica con la claridad y la mantenibilidad, y a valorar la importancia de la documentación y el control de versiones para no perder el progreso logrado.

---

## 📈 Próximos Pasos

| Fase                | Tareas                                              |
| ------------------- | --------------------------------------------------- |
| Feature Engineering | Binning edad, encoding categóricas, ratio contactos |
| Modelado            | Baseline (LogReg), árboles (RF, XGBoost), tuning    |
| Evaluación          | AUC, Recall, Precision, curva ganancias             |
| Deployment          | FastAPI + Streamlit (dashboard)                     |

---

## 🛠 Tecnologías

Python 3.10+ · pandas · numpy · seaborn · matplotlib · openpyxl · Jupyter · fpdf2 · statsmodels

---

## 🗂 Documentación

- [docs/especificaciones_proyecto.md](docs/especificaciones_proyecto.md)
- [reports/documentacion/informe_ejecutivo.md](reports/documentacion/informe_ejecutivo.md)
- [reports/outputs/analisis_demografico_completo.txt](reports/outputs/analisis_demografico_completo.txt)

---

## 🧪 Reproducibilidad Notebook

Si no se instaló el paquete en modo editable (`pip install -e .`):

```python
import sys, os
project_root = os.path.dirname(os.getcwd())
if project_root not in sys.path:
    sys.path.append(project_root)
```

---

## 👤 Autor

Andrea Gicela Bravo Landeta

Repositorio: https://github.com/roseprogramming/eda_marqueting_bancario

---

## 📅 Última actualización

Febrero 2026

---

### Sobre la documentación

La documentación de este proyecto se ha hecho especialmente exhaustiva para no perderme yo misma durante el desarrollo y para no olvidar detalles importantes en el futuro. Este esfuerzo me ha servido mucho para entender mejor cada paso, justificar decisiones y poder retomar el trabajo en cualquier momento sin confusión.

---
