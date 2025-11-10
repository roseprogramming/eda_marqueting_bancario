# Informe Ejecutivo: EDA Marketing Bancario

Proyecto: Predicción de suscripción a depósitos a plazo  
Periodo analizado: 2012–2014  
Fecha de actualización: 10/11/2025

---

## 1) Resumen ejecutivo

El análisis exploratorio consolida un “Master Dataset” con información de:

- Perfil del cliente (edad, educación, ocupación, estado civil).
- Historial y contexto de campaña (contacto, resultado previo, frecuencia).
- Indicadores macro (emp_var_rate, euribor3m, cons_price_idx).
- Derivadas clave (antiguedad_años, segmento_edad, previous_contact).

Hallazgos de alto nivel:

- El resultado de campaña previa (poutcome) discrimina fuertemente la probabilidad de suscripción.
- La antigüedad del cliente y la edad muestran patrones consistentes (segmentos mayores y con antigüedad baja-moderada responden mejor).
- Income y composición del hogar aportan señal débil en este contexto.
- duration es data leakage y no debe usarse en modelos de scoring pre-contacto.

El análisis detallado y salidas textuales se encuentran en:

- reports/outputs/analisis_demografico_completo.txt

---

## 2) Proceso de limpieza (resumen)

Origen de datos:

- data/raw/bank-additional.csv (campaña)
- data/raw/customer-details.xlsx (2012, 2013, 2014)

Transformaciones principales:

- Normalización de nombres a snake_case (dc.clean_column_names).
- Conversión de tipos y estandarización de separadores decimales.
- Recodificación de y (yes/no → 1/0) y creación de previous_contact (pdays != 999).
- Unificación y join por id para construir df_perfil_cliente.
- Variables derivadas: antiguedad_años, segmento_edad.

Detalles técnicos completos:

- reports/documentacion/archive/informe_preliminar.md

---

## 3) Insights clave

3.1 Demografía

- Edad: los segmentos senior presentan mayor conversión que los jóvenes.
- Educación: mayor nivel educativo tiende a mejorar la tasa.
- Ocupación: “retired”, “student” y roles profesionales suelen superar la media; “blue-collar” y “services” suelen estar por debajo.

  3.2 Campaña

- poutcome=success incrementa fuertemente la probabilidad de suscripción.
- campaign (número de contactos) y previous_contact ayudan a contextualizar saturación y eficacia.
- contact (canal) y estacionalidad temporal (month, day_of_week) muestran diferencias aprovechables en planificación.

  3.3 Macroeconómicas

- emp_var_rate y euribor3m suelen correlacionar con propensión a suscribir (relación inversa en fases recesivas vs expansivas).
- cons_price_idx aporta información con efecto moderado; revisar colinealidad entre indicadores.

  3.4 Variables con baja señal

- income, kidhome, teenhome muestran poder predictivo limitado en este problema.

---

## 4) Data leakage

Variable afectada:

- duration: solo se conoce tras finalizar la llamada.

Implicación:

- No usar duration en modelos de scoring previos al contacto.
- Útil para análisis post-mortem (optimización de guiones y tiempos de llamada).

---

## 5) Recomendaciones para modelado

Conjunto sugerido de variables (ejemplo base):

- Demográficas: age, education, job, marital
- Campaña: poutcome, contact, campaign, previous_contact
- Temporales: contact_month, contact_day_of_week
- Macros: emp_var_rate, euribor3m, cons_price_idx
- Derivadas: antiguedad_años

Excluir de entrada:

- income, kidhome, teenhome, duration (por leakage)

Buenas prácticas:

- One-hot/target encoding para categóricas (evaluar fuga de información).
- Revisión de colinealidad (VIF) en indicadores macro.
- Validación estratificada y seguimiento de métricas sensibles a clase (AUC, Recall, Precision, PR-AUC).

---

## 6) Segmentación operativa (orientativa)

- Alta prioridad: clientes con éxito previo (poutcome=success), edad media-alta, antigüedad < 4 años.
- Media prioridad: perfiles profesionales sin contacto previo o con resultado neutro.
- Baja prioridad: segmentos jóvenes con histórico de failure reciente.

Ajustar umbrales con base en costes y capacidad operativa (curvas de ganancias y lift).

---

## 7) Próximos pasos

1. Feature engineering

- Binning óptimo de age y antiguedad_años (WoE/Monotonicidad).
- Variables de intensidad: ratio_contacts (campaign/pdays, cuando aplique).
- Encoding robusto para alta cardinalidad (target/GLMM encoding con CV interna).

2. Modelado

- Baselines: Logistic Regression (interpretabilidad).
- Árboles/Boosting: Random Forest, XGBoost/LightGBM (tabular).
- Búsqueda de hiperparámetros con validación cruzada estratificada.

3. Evaluación y despliegue

- Matrices de confusión por segmento y umbral optimizado por coste.
- Curvas de ganancias y uplift para priorización operativa.
- Versionado del pipeline y endpoints de scoring (FastAPI) + dashboard (Streamlit).

---

## 8) Trazabilidad y artefactos

- Notebook principal: notebooks/01_EDA_Analisis.ipynb
- Datasets procesados: data/processed/
  - df_campaign_clean.csv
  - df_customer_details.csv
  - df_perfil_cliente.csv
- Salidas de análisis: reports/outputs/analisis_demografico_completo.txt
- Detalles técnicos: reports/documentacion/archive/informe_preliminar.md

---
