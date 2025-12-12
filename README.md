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

**Resultado:** Pipeline ETL completo, análisis exploratorio exhaustivo con 7 visualizaciones, identificación de segmentos de alto valor y detección de data leakage, todo documentado en informes ejecutivos listos para decisiones de negocio.

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

- 7 gráficos clave (distribuciones, tasas, correlaciones)
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
│   └── 01_EDA_Analisis.ipynb  # Notebook principal de análisis
├── src/
│   ├── pipeline.py                 # Pipeline completo
│   ├── analisis_exploratorio.py
│   ├── data_cleaning.py
│   ├── cleaning_campaing.py
│   └── plotting.py                 # Funciones de visualización
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

---

## 🚀 Instalación

```bash
git clone https://github.com/roseprogramming/eda_marqueting_bancario.git
cd eda_marqueting_bancario
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Los datasets ya están incluidos en el repositorio.
Abrir y ejecutar: notebooks/01_EDA_Analisis.ipynb

## ⚡ Ejecutar Pipeline (Simple)

Desde terminal:

```cmd
cd tu\proyecto
".venv\Scripts\python.exe" src/pipeline.py --profile
```

**Eso es todo.** Genera 3 CSVs:

- `df_campaign_clean.csv` — Campaña limpia (8.6 MB)
- `df_customer_details.csv` — Clientes 2012-2014 (2.9 MB)
- `df_perfil_cliente.csv` ⭐ — **Master dataset (usa este en notebook)**

---

## 📝 Código del Pipeline

El archivo `src/pipeline.py` contiene:

- Lectura de CSV y Excel
- Limpieza de tipos, fechas, nombres
- Recodificación de variables especiales
- Unión de datasets por `id`

**Ver archivo:** [src/pipeline.py](src/pipeline.py)

---

## 📊 Informe del Análisis

### Estadísticas Clave

- **Dataset final:** 43,000 registros × 30 variables
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
- Retraso: 30 minutos en la sesión final

### 9. **Decisiones Arquitectónicas Sin Claridad**

- ¿Guardar datos procesados en CSV o memoria?
- ¿Qué hacer con valores faltantes? (mean/median/drop)
- ¿Cuántas visualizaciones son "suficientes"?
- Solución: **Documentar decisiones en docstrings y comments**

---

## �📦 Variables recomendadas para modelado

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

## 📈 Próximos Pasos

| Fase                | Tareas                                              |
| ------------------- | --------------------------------------------------- |
| Feature Engineering | Binning edad, encoding categóricas, ratio contactos |
| Modelado            | Baseline (LogReg), árboles (RF, XGBoost), tuning    |
| Evaluación          | AUC, Recall, Precision, curva ganancias             |
| Deployment          | FastAPI + Streamlit (dashboard)                     |

---

## 🛠 Tecnologías

Python 3.13 · pandas · numpy · seaborn · matplotlib · openpyxl · Jupyter

---

## 🗂 Documentación

- [docs/especificaciones_proyecto.md](docs/especificaciones_proyecto.md)
- [reports/documentacion/informe_ejecutivo.md](reports/documentacion/informe_ejecutivo.md)
- [reports/outputs/analisis_demografico_completo.txt](reports/outputs/analisis_demografico_completo.txt)

---

## 🧪 Reproducibilidad Notebook

Si módulos no cargan:

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

Diciembre 2025
