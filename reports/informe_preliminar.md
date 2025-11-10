# Informe Preliminar: Análisis Exploratorio de Datos - Campaña de Marketing Bancario

## 1. Introducción

Este documento presenta el análisis exploratorio inicial de los datasets relacionados con campañas de marketing bancario. El objetivo es evaluar la calidad de los datos, identificar problemas estructurales y documentar el proceso de limpieza previo al análisis estadístico detallado.

El proyecto trabaja con dos fuentes principales: bank-additional.csv con datos de campaña telefónica (43,000 registros) y customer-details.xlsx con información demográfica de clientes distribuida en tres hojas anuales 2012-2014 (43,170 registros combinados).

---

## 2. Problemas Identificados en Datos Crudos

### 2.1 Dataset de Campaña

El dataset original presentó múltiples problemas de calidad: variables numéricas (cons.price.idx, cons.conf.idx, euribor3m, nr.employed) incorrectamente tipadas como object, campo age almacenado como float con valores faltantes cuando debería ser int, campo date en formato object en lugar de datetime, y variable objetivo y como texto (yes/no) en lugar de binario numérico. La nomenclatura era inconsistente (id\_, cons.price.idx) y existía un marcador especial pdays=999 para indicar "nunca contactado".

Los valores faltantes más significativos afectaban a default (21%), euribor3m (22%), age (12%), education (4%) y housing/loan (2%). Adicionalmente, se identificaron columnas latitude y longitude sin justificación analítica clara para el contexto bancario.

### 2.2 Dataset de Detalles de Cliente

Este dataset mostró mejor calidad estructural pero requería consolidación: información fragmentada en tres hojas Excel sin unificar y nomenclatura inconsistente (mezcla de mayúsculas/minúsculas, variable NumWebVisitsMonth sin separadores). No se detectaron valores faltantes ni inconsistencias de formato.

---

## 3. Proceso de Limpieza Aplicado

### 3.1 Limpieza de Dataset de Campaña

Se implementó un módulo especializado (cleaning_campaing.py) que corrigió tipos de datos convirtiendo variables numéricas mal tipadas, transformó age a int64 tras imputación y parseó date a datetime64[ns]. Se recodificó la variable objetivo y de texto a binario (1/0) y se creó una bandera previous_contact para manejar el marcador especial pdays=999.

Los valores faltantes se trataron mediante imputación por moda en categóricas (education, marital) y mediana en numéricas (age, euribor3m). Las variables categóricas se optimizaron al tipo category para mejorar rendimiento y reducir memoria. Se aplicó nomenclatura PEP 8 en snake*case renombrando id* a id, cons.price.idx a cons_price_idx, entre otras. Finalmente se eliminaron las columnas latitude y longitude por falta de relevancia analítica.

El resultado es df_campaign_clean con 43,000 registros y 24 variables correctamente tipadas (se añade previous_contact como nueva variable).

### 3.2 Limpieza de Dataset de Detalles de Cliente

Se consolidaron las tres hojas temporales mediante concatenación vertical con pd.concat(), creando una columna year como marcador temporal convertida a tipo category. Se aplicó normalización automática mediante clean_column_names() del módulo data_cleaning.py y corrección manual de numwebvisitsmonth a num_web_visits_month. Se verificó la ausencia de valores faltantes, la unicidad de identificadores y la correcta tipificación de variables.

El resultado es df_customer_details con 43,170 registros y 7 variables incluyendo year como nueva columna categórica.

---

## 4. Estado Post-Limpieza

### 4.1 Dataset df_campaign_clean

El proceso de limpieza produjo un dataset estructurado con 43,000 registros y 24 variables correctamente tipadas aplicando estándares PEP 8 en nomenclatura, optimizando variables categóricas mediante tipo category, normalizando indicadores económicos y recodificando el target de texto a binario numérico. Las variables temporales quedaron en formato datetime64[ns] permitiendo análisis de estacionalidad y se creó la bandera previous_contact para el marcador pdays=999.

Las variables se agrupan en: target y (binario 0/1 listo para clasificación), perfil demográfico (age, job, marital, education sin faltantes), situación financiera (default, housing, loan categóricas optimizadas), contexto económico (emp_var_rate, cons_price_idx, cons_conf_idx, euribor3m, nr_employed normalizadas pero potencialmente correlacionadas), historial de campaña (poutcome, previous_contact, campaign, previous como predictores relevantes), variables temporales (date, contact_month, contact_year en formatos estándar) y duration marcada para exclusión por data leakage.

Se identificaron alertas críticas: desbalance severo de clases con tasa de éxito del 11% requiriendo técnicas de balanceo como SMOTE, probable multicolinealidad entre variables económicas a confirmar mediante matriz de correlación, posible efecto de estacionalidad en contact_month, y exclusión obligatoria de duration en modelado por conocerse solo post-resultado.

### 4.2 Dataset df_customer_details

El dataset consolidado presenta 43,170 registros con 7 variables correctamente tipadas siguiendo nomenclatura PEP 8, incluyendo la corrección manual de num_web_visits_month. Las variables temporales están en datetime64[ns] (dt_customer), year convertida a category, y variables numéricas en int64. No presenta valores faltantes, outliers críticos ni inconsistencias de formato confirmando origen transaccional robusto.

Los identificadores son únicos garantizando uniones fiables con df_campaign_clean. Las distribuciones de income, kidhome, teenhome y num_web_visits_month son coherentes con perfiles bancarios reales. Se identificó concentración desigual de registros por año (mayor proporción en 2012) que debe considerarse en análisis temporales para evitar sesgos de representatividad.

---

## 5. Integración de Datasets

Se realizó inner join utilizando id como clave normalizada, resultando en el dataset maestro df_perfil_cliente con 43,000 registros y 30 variables. La integración combina 24 columnas del dataset de campaña más 6 del dataset de clientes excluyendo id duplicado. Se verificó coincidencia uno a uno entre identificadores sin pérdida de registros y preservación de tipos de datos. El dataset se exportó a ../data/processed/df_perfil_cliente.csv para análisis posteriores.

---

## 6. Próximos Pasos

El análisis exploratorio profundo incluirá distribuciones univariadas mediante histogramas y boxplots, frecuencias de categóricas y detección de outliers por IQR. El análisis bivariado examinará relación de variables con el target, tasas de conversión por segmentos y correlaciones numéricas. El multivariado construirá matriz de correlación completa, detectará multicolinealidad mediante VIF y evaluará pertinencia de PCA.

El feature engineering creará antiguedad_cliente (date - dt_customer), aplicará binning en variables continuas si mejora interpretabilidad, generará interacciones relevantes y codificará categóricas mediante one-hot o label encoding. La preparación para modelado evaluará desbalance de clases aplicando SMOTE o undersampling, dividirá datos en train/validation/test, estandarizará variables numéricas y aplicará selección de features.

Los archivos generados son: df_campaign_clean.csv (dataset de campaña limpio), df_customer_details.csv (dataset de clientes consolidado) y df_perfil_cliente.csv (dataset maestro integrado), todos ubicados en ../data/processed/.

---

## 7. Conclusiones

El proceso de limpieza produjo datasets de alta calidad listos para análisis estadístico y modelado predictivo. La normalización según PEP 8, corrección de tipos y tratamiento sistemático de faltantes garantizan reproducibilidad y fiabilidad del análisis.

Los datasets permiten abordar preguntas de negocio relevantes: identificar factores que influyen en probabilidad de suscripción, detectar perfiles con mayor propensión a aceptar ofertas, y evaluar cómo condiciones económicas impactan el éxito de campañas. La calidad documentada establece base sólida para modelado y generación de insights accionables para estrategia de marketing bancario.
