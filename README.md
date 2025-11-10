# PROYECTO: EDA con Python - Marketing Bancario

## Análisis Exploratorio de Datos aplicado a Campañas de Marketing Bancario

**Entrega correspondiente al módulo "Python for Data" del Máster en Data & Analytics**

---

## Descripción del Proyecto

Este proyecto realiza un **Análisis Exploratorio de Datos (EDA)** completo sobre datos de campañas de marketing bancario, con el objetivo de identificar patrones y características de clientes que determinan el éxito en la contratación de depósitos a plazo.

El análisis combina datos de campañas telefónicas con perfiles demográficos de clientes para construir un **dataset maestro** (`df_perfil_cliente`) optimizado para modelado predictivo.

---

## Objetivos

1. **Limpiar y normalizar** múltiples fuentes de datos bancarios
2. **Integrar** información de campañas con perfiles de clientes
3. **Identificar variables clave** que influyen en la suscripción de productos
4. **Generar insights accionables** para segmentación de marketing
5. **Preparar datos** para modelado predictivo posterior

---

## Estructura del Proyecto

EDA_Marketing_Bancario/
│
├── .vscode/
│ └── [settings.json](./.vscode/settings.json) # Configuración de VS Code (portable)
│
├── data/
│ ├── raw/ # Datos originales (no modificar)
│ │ ├── [bank-additional.csv](./data/raw/bank-additional.csv) # Datos de campaña bancaria
│ │ └── [customer-details.xlsx](./data/raw/customer-details.xlsx) # Perfiles de clientes (2012-2014)
│ │
│ └── processed/ # Datos procesados y listos para análisis
│ ├── [df_campaign_clean.csv](./data/processed/df_campaign_clean.csv)
│ ├── [df_customer_details.csv](./data/processed/df_customer_details.csv)
│ └── [df_perfil_cliente.csv](./data/processed/df_perfil_cliente.csv) # Dataset maestro final
│
├── notebooks/
│ └── [01_EDA_Analisis.ipynb](./notebooks/01_EDA_Analisis.ipynb) # Notebook principal de análisis
│
├── src/ # Módulos personalizados
│ ├── [**init**.py](./src/__init__.py)
│ ├── [analisis_exploratorio.py](./src/analisis_exploratorio.py) # Funciones de análisis (tasas, proporciones)
│ ├── [data_cleaning.py](./src/data_cleaning.py) # Limpieza y normalización general
│ └── [cleaning_campaing.py](./src/cleaning_campaing.py) # Limpieza específica de datos de campaña
│
├── reports/
│ └── [informe_preliminar.md](./reports/informe_preliminar.md) # Documentación de hallazgos
│
├── [requirements.txt](./requirements.txt) # Dependencias del proyecto
└── README.md # Este archivo

---

## Instalación y Configuración

### Requisitos Previos

- Python 3.9+
- pip (gestor de paquetes)
- Visual Studio Code (recomendado)

### Pasos de Instalación

1. **Clonar el repositorio**
   bash
   git clone <url-del-repositorio>
   cd EDA_Marketing_Bancario
2. **Crear entorno virtual**
   bash
   python -m venv .venv
3. **Activar el entorno virtual**
   - **Windows:**
     bash
     .venv\Scripts\activate
   - **Mac/Linux:**
     bash
     source .venv/bin/activate
4. **Instalar dependencias**
   bash
   pip install -r requirements.txt
5. **Abrir en VS Code**
   bash
   code .
6. **Seleccionar intérprete de Python**

   - `Ctrl+Shift+P` → `Python: Select Interpreter`
   - Seleccionar `.venv/Scripts/python.exe`

7. **Ejecutar el notebook**
   - Abrir `notebooks/01_EDA_Analisis.ipynb`
   - Ejecutar celdas secuencialmente

---

## Datasets Utilizados

### 1. **bank-additional.csv** - Datos de Campaña

- **Registros:** ~41,000 contactos telefónicos
- **Variables:** 21 columnas (demográficas, económicas, historial de contacto)
- **Target:** `y` (suscripción a depósito: yes/no)
- **Problemas identificados:**
  - Columnas numéricas leídas como `object` (`cons.price.idx`, `euribor3m`, etc.)
  - Valores faltantes (~22% en variables económicas)
  - Nombres no normalizados (`id_`, `cons.conf.idx`)
  - Marcador especial `pdays=999` (nunca contactado)

### 2. **customer-details.xlsx** - Perfiles de Clientes

- **Hojas:** 3 (años 2012, 2013, 2014)
- **Registros:** ~30,000 clientes únicos
- **Variables:** ID, Income, Kidhome, Teenhome, Dt_Customer
- **Estado:** Dataset limpio, sin valores faltantes

---

## Pipeline de Procesamiento

### Fase 1: Limpieza Individual

```python
# Campaign Data
df_campaign_clean = cc.clean_campaign_df(df_campaign)
df_campaign_clean = dc.clean_column_names(df_campaign_clean)
# Customer Details
df_customer_details = pd.concat([df_2012, df_2013, df_2014])
df_customer_details = dc.normalizar_nombres_columnas(df_customer_details)
```

### Fase 2: Integración

```python
df_perfil_cliente = pd.merge(
    df_campaign_clean,
    df_customer_details,
    on='id',
    how='inner'
)
```

### Fase 3: Feature Engineering

- Creación de variable `antiguedad_dias`
- Variable binaria `tiene_hijos`
- Normalización de nombres a **snake_case** (PEP 8)

---

## Principales Hallazgos

### 1. **Ingreso vs. Suscripción**

- **El ingreso NO es predictor significativo**
- Ratio de medias (éxito/fracaso): ~1.02
- Conclusión: La propensión a suscribir no depende del poder adquisitivo

### 2. **Antigüedad del Cliente**

- **Variable clave identificada**
- Clientes que suscriben: **~3.5 años** de antigüedad
- Clientes que rechazan: **~4.2 años** de antigüedad
- **Insight:** Clientes más recientes son más receptivos

### 3. **Composición del Hogar**

- **Variables `kidhome` y `teenhome` irrelevantes**
- Tasa de suscripción estable: **~11.3%** en todas las categorías
- No usar para segmentación

### 4. **Duración de Llamada**

- **Data Leakage:** No usar en modelos predictivos
- Fuerte correlación con éxito (consecuencia, no causa)

### 5. **Resultado de Campaña Anterior (`poutcome`)**

- **Predictor potente**
- Clientes con éxito previo: alta propensión a repetir

---

## Módulos Personalizados

### `data_cleaning.py`

```python
# Normalización de nombres de columnas
normalizar_nombres_columnas(df, verbose=True)
# Validación completa de datos
run_checks(df, posibles_cat=['education', 'marital'])
```

### `analisis_exploratorio.py`

```python
# Cálculo de tasas de suscripción por categoría
calcular_tasa_proporciones(df, 'variable_categorica')
# Retorna: DataFrame con [variable, total, exitos, tasa_exito]
```

### `cleaning_campaing.py`

```python
# Limpieza específica de datos de campaña
clean_campaign_df(df)
# - Conversión de tipos
# - Tratamiento de valores faltantes
# - Recodificación de target
```

---

## Buenas Prácticas Implementadas

### 1. **Normalización de Nombres (PEP 8)**

- Todo en `snake_case`: `cons_price_idx`, `dt_customer`, `tasa_exito`
- Evitado: `PascalCase`, `camelCase`, `MAYÚSCULAS`

### 2. **Modularización**

- Código reutilizable en `src/`
- Separación de responsabilidades
- Documentación con docstrings

### 3. **Reproducibilidad**

- Configuración portable (`.vscode/settings.json`)
- `requirements.txt` con versiones
- Estructura estándar de proyecto

### 4. **Control de Calidad**

- Validaciones automáticas (`run_checks`)
- Detección de data leakage
- Análisis post-limpieza

---

## Conclusiones Estratégicas

### Perfil del Cliente Exitoso

- **Antigüedad:** 3-4 años con el banco
- **Historial:** Éxito en campañas anteriores
- **Ingreso:** Irrelevante (no discrimina)
- **Hogar:** Composición familiar no influye

### Recomendaciones de Marketing

1. **Priorizar clientes recientes** (< 4 años de antigüedad)
2. **No segmentar por nivel de ingresos**
3. **Aprovechar historial positivo** de campañas anteriores
4. **Evitar variables de hogar** para scoring

### Variables para Modelado Predictivo

- **Incluir:** `antiguedad_dias`, `poutcome`, indicadores económicos
- **Usar con cautela:** `duration` (data leakage)
- **Excluir:** `income`, `kidhome`, `teenhome`

---

## Configuración Técnica

### VS Code Settings (`.vscode/settings.json`)

```json
{
  "python.analysis.extraPaths": [
    "${workspaceFolder}",
    "${workspaceFolder}/src"
  ],
  "jupyter.notebookFileRoot": "${workspaceFolder}",
  "python.analysis.typeCheckingMode": "basic"
}
```

### Requirements.txt

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
openpyxl>=3.1.0
jupyter>=1.0.0
```

---

## Contacto y Contribuciones

- **Autor:** Andrea Gicela Bravo Landeta
- **Máster:** Data & Analytics
- **Módulo:** Python for Data

Para consultas o sugerencias, abrir un **issue** en el repositorio.

---

## Licencia

Este proyecto es material académico del Máster en Data & Analytics en la escuela thePower FP.

---

## Roadmap Futuro

- [ ] Modelado predictivo (Logistic Regression, Random Forest)
- [ ] Dashboard interactivo con Streamlit
- [ ] Análisis de series temporales de campañas
- [ ] Optimización de segmentación con clustering
- [ ] Implementación de pipelines con scikit-learn

---

**Última actualización:** Noviembre 2025
