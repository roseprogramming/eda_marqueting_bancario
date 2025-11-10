# 📊 EDA Marketing Bancario

Análisis Exploratorio de Datos (EDA) sobre campañas de marketing bancario para identificar patrones que influyen en la suscripción de depósitos a plazo.

**Máster Data & Analytics – Módulo: Python for Data**

---

## 🎯 Objetivo

Construir un dataset maestro limpio y documentado que permita:

- Detectar perfiles con mayor tasa de conversión.
- Identificar variables predictivas útiles.
- Evitar uso de variables con data leakage.
- Preparar una base sólida para futuros modelos.

---

## 📁 Estructura

```
EDA_Marketing_Bancario/
├── data/                # Incluido en Git (28.8 MB total)
│   ├── raw/             # bank-additional.csv, customer-details.xlsx
│   └── processed/       # df_campaign_clean.csv, df_customer_details.csv, df_perfil_cliente.csv
├── notebooks/
│   └── 01_EDA_Analisis.ipynb
├── src/
│   ├── analisis_exploratorio.py
│   ├── data_cleaning.py
│   └── cleaning_campaing.py
├── reports/
│   ├── outputs/         # analisis_demografico_completo.txt
│   └── documentacion/
│       ├── informe_ejecutivo.md
│       └── archive/
│           └── informe_preliminar.md
├── docs/
│   ├── especificaciones_proyecto.md
├── requirements.txt
└── README.md
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

---

## 🔄 Pipeline

1. Carga de datos (campaña + perfiles clientes).
2. Limpieza específica campaña (tipos, recodificación, previous_contact).
3. Normalización nombres (snake_case).
4. Integración en df_perfil_cliente.
5. Feature engineering (antiguedad_años, segmento_edad).
6. Análisis demográfico y de campaña.
7. Exportación de reportes a reports/outputs/.

---

## 🧪 Principales Hallazgos

| Insight                         | Resultado                    | Acción                 |
| ------------------------------- | ---------------------------- | ---------------------- |
| Edad avanzada (56–65)           | Tasa > 18%                   | Priorizar segmentación |
| Éxito previo (poutcome=success) | Tasa ~65%                    | Lista premium          |
| Antigüedad < 4 años             | Mayor receptividad           | Enfoque inicial        |
| Income                          | No discrimina (ratio ~1.02x) | Excluir del modelo     |
| duration                        | Data leakage                 | No usar en scoring     |

---

## ⚠ Data Leakage

Variable duration solo conocida tras la llamada. Usar solo en análisis post-mortem, nunca en modelos predictivos previos al contacto.

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

## 📈 Próximos Pasos

| Fase                | Tareas                                              |
| ------------------- | --------------------------------------------------- |
| Feature Engineering | Binning edad, encoding categóricas, ratio contactos |
| Modelado            | Baseline (LogReg), árboles (RF, XGBoost), tuning    |
| Evaluación          | AUC, Recall, Precision, curva ganancias             |
| Deployment          | FastAPI + Streamlit (dashboard)                     |

---

## 🛠 Tecnologías

Python 3.11 · pandas · numpy · seaborn · matplotlib · openpyxl · Jupyter

---

## 🗂 Documentación

- docs/especificaciones_proyecto.md
- reports/documentacion/informe_ejecutivo.md
- reports/outputs/analisis_demografico_completo.txt

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

## 🧹 Mantenimiento

```bash
# Eliminar cachés
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type d -name ".ipynb_checkpoints" -exec rm -r {} +

# Ver árbol (Windows sin tree instalado)
dir /s /b
```

---

## 👤 Autor

Andrea Gicela Bravo Landeta

Repositorio: https://github.com/roseprogramming/eda_marqueting_bancario

---

## 📅 Última actualización

Noviembre 2025

---
