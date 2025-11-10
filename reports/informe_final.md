INSIGHTS CLAVE DEL ANÁLISIS EXPLORATORIO
Hallazgos Principales del Dataset df_perfil_cliente

==========================================================
INSIGHT 1: INGRESO NO DISCRIMINA ÉXITO
==========================================================

HALLAZGO:
El ratio de ingresos medios entre clientes exitosos (y=1) y no exitosos (y=0)
es prácticamente 1.02, lo que indica que NO HAY diferencia significativa.

IMPLICACIÓN ESTRATÉGICA:

- NO segmentar campañas por nivel de ingresos
- El poder adquisitivo NO predice la contratación del depósito
- Democratizar la oferta a todos los segmentos económicos

ACCIÓN RECOMENDADA:
Eliminar Income como variable predictiva en modelos de scoring.
Enfocar recursos en otras variables más discriminantes.

==========================================================
INSIGHT 2: ANTIGÜEDAD DEL CLIENTE ES CLAVE
==========================================================

HALLAZGO:
Clientes exitosos: ~3.5 años de antigüedad (1,277 días)
Clientes no exitosos: ~4.2 años de antigüedad (1,533 días)
Diferencia: ~256 días (8.5 meses)

IMPLICACIÓN ESTRATÉGICA:

- Clientes MÁS RECIENTES tienen mayor propensión a contratar
- La "ventana de oportunidad" está en los primeros 3-4 años
- Clientes antiguos ya están consolidados (menor receptividad)

SEGMENTACIÓN PROPUESTA:

- Segmento HOT: < 3 años de antigüedad (prioridad máxima)
- Segmento WARM: 3-5 años (estrategia moderada)
- Segmento COLD: > 5 años (bajo esfuerzo comercial)

ACCIÓN RECOMENDADA:
Crear variable binaria: cliente_reciente = antiguedad_dias < 1095 (3 años)
Usar como filtro principal en campañas outbound.

==========================================================
INSIGHT 3: COMPOSICIÓN DEL HOGAR ES IRRELEVANTE
==========================================================

HALLAZGO:
Tasa de suscripción ESTABLE (~11.3%) independientemente de:

- Presencia/ausencia de hijos (tiene_hijos)
- Número de niños en casa (kidhome: 0, 1, 2, 3)
- Número de adolescentes (teenhome: 0, 1, 2)

CONTRADICCIÓN CON INTUICIÓN:
Se esperaba que hogares SIN dependientes tuvieran:

- Mayor renta disponible
- Mayor propensión a ahorrar
  PERO los datos NO confirman esta hipótesis.

ACCIÓN RECOMENDADA:
EXCLUIR variables kidhome y teenhome de modelos predictivos.
NO usar composición del hogar para priorización de leads.
Liberar recursos de segmentación demográfica tradicional.

==========================================================
INSIGHT 4: DATA LEAKAGE CONFIRMADO EN DURATION
==========================================================

HALLAZGO:
Duración media de llamada:

- Éxito (y=1): ~550 segundos (9+ minutos)
- Fracaso (y=0): ~220 segundos (3.5 minutos)

PROBLEMA CRÍTICO:
La duración de llamada es una CONSECUENCIA del resultado, NO una causa:

- Llamadas exitosas son largas PORQUE el cliente acepta (se explica el producto)
- Llamadas fallidas son cortas PORQUE el cliente rechaza rápido

RIESGO DE MODELADO:
Si se incluye duration en un modelo predictivo:

- El modelo "haría trampa" usando información del futuro
- Precisión artificialmente inflada (overfitting)
- Inútil en producción (no se conoce duration ANTES de llamar)

ACCIÓN RECOMENDADA:

- USAR duration solo para análisis descriptivo/post-mortem
- EXCLUIR duration de cualquier modelo de scoring pre-contacto
- Documentar explícitamente este data leakage en informes

==========================================================
INSIGHT 4: DATA LEAKAGE CONFIRMADO EN DURATION
==========================================================

HALLAZGO:
Duración media de llamada:

- Éxito (y=1): ~550 segundos (9+ minutos)
- Fracaso (y=0): ~220 segundos (3.5 minutos)

PROBLEMA CRÍTICO:
La duración de llamada es una CONSECUENCIA del resultado, NO una causa:

- Llamadas exitosas son largas PORQUE el cliente acepta (se explica el producto)
- Llamadas fallidas son cortas PORQUE el cliente rechaza rápido

RIESGO DE MODELADO:
Si se incluye duration en un modelo predictivo:

- El modelo "haría trampa" usando información del futuro
- Precisión artificialmente inflada (overfitting)
- Inútil en producción (no se conoce duration ANTES de llamar)

ACCIÓN RECOMENDADA:

- USAR duration solo para análisis descriptivo/post-mortem
- EXCLUIR duration de cualquier modelo de scoring pre-contacto
- Documentar explícitamente este data leakage en informes

==========================================================
INSIGHT 5: HISTORIAL DE CAMPAÑA ANTERIOR (poutcome)
==========================================================

HALLAZGO ESPERADO (verificar con datos):
poutcome (resultado de campaña previa) probablemente muestra:

- "success" → Tasa de conversión MUY ALTA (posible 30-50%)
- "failure" → Tasa de conversión BAJA (~5-10%)
- "nonexistent" → Tasa intermedia (~11-12%)

FENÓMENO: "Éxito atrae éxito"
Clientes que contrataron antes tienen ALTA propensión a repetir.

IMPLICACIÓN ESTRATÉGICA:

- Crear segmento VIP: clientes con poutcome = "success"
- Campañas de fidelización para maximizar repeat rate
- Ofertas premium para este segmento (ya validado)

ACCIÓN RECOMENDADA:
Priorizar contacto con clientes poutcome="success"
Diseñar journey diferenciado para este segmento.

==========================================================
INSIGHT 6: DESBALANCE DE CLASES (TARGET y)
==========================================================

HALLAZGO CRÍTICO (verificar proporción exacta):
Si la tasa general de éxito es ~11.3%, entonces:

- Clase mayoritaria (y=0): ~88.7% (35,000+ registros)
- Clase minoritaria (y=1): ~11.3% (4,500+ registros)

RATIO: ~8:1 (desbalance severo)

PROBLEMA PARA MODELADO:

- Modelos tenderán a predecir siempre "No suscribe"
- Métrica accuracy será engañosa (88% por predecir todo a 0)
- Se perderán patrones de la clase minoritaria

SOLUCIONES NECESARIAS:

1. Técnicas de balanceo:

   - SMOTE (Synthetic Minority Over-sampling)
   - Class weights en algoritmos (penalizar errores en y=1)
   - Undersampling controlado de clase mayoritaria

2. Métricas adecuadas:
   - NO usar accuracy
   - SÍ usar: Precision, Recall, F1-Score, AUC-ROC
   - Enfocarse en capturar verdaderos positivos (y=1)

ACCIÓN RECOMENDADA:
Implementar SMOTE o class_weight='balanced' en modelos.
Evaluar con confusion matrix y curva ROC.

==========================================================
INSIGHT 7: VARIABLES ECONÓMICAS (Potencial Correlación)
==========================================================

VARIABLES EN JUEGO:

- emp_var_rate: Tasa variación empleo
- cons_price_idx: Índice precios consumidor
- cons_conf_idx: Índice confianza consumidor
- euribor3m: Tasa Euribor 3 meses
- nr_employed: Número empleados (trimestral)

HIPÓTESIS A VERIFICAR:
Estas 5 variables probablemente están ALTAMENTE correlacionadas porque:

- Todas miden contexto macroeconómico
- Se mueven juntas en ciclos económicos
- Capturan el mismo fenómeno (situación económica general)

RIESGO: MULTICOLINEALIDAD
Si correlación > 0.8 entre ellas:

- Modelos lineales inestables (coeficientes erróneos)
- Dificultad para interpretar importancia individual
- Redundancia de información

ACCIÓN RECOMENDADA INMEDIATA:

1. Calcular matriz de correlación:
   df_perfil_cliente[['emp_var_rate', 'cons_price_idx', 
                   'cons_conf_idx', 'euribor3m', 
                   'nr_employed']].corr()

2. Si correlación > 0.8:
   - Reducir a 1-2 variables representativas (PCA o selección manual)
   - Crear índice compuesto económico
   - Usar solo euribor3m (más interpretable)

==========================================================
INSIGHT 8: ESTACIONALIDAD TEMPORAL (contact_month)
==========================================================

HIPÓTESIS A EXPLORAR:
El mes de contacto (contact_month) puede influir por:

- Comportamiento estacional del consumidor
- Disponibilidad de liquidez (ej: pagas extras en junio/diciembre)
- Períodos vacacionales (menor receptividad)
- Cierre fiscal (mayor propensión a ahorrar)

MESES ESPERADOS CON ALTA CONVERSIÓN:

- Enero: Propósitos año nuevo, bonos navideños residuales
- Junio/Julio: Paga extra verano
- Diciembre: Paga extra navidad + planificación fiscal

MESES ESPERADOS CON BAJA CONVERSIÓN:

- Agosto: Vacaciones (menor disponibilidad)
- Febrero-Abril: Post-gastos navideños

ACCIÓN RECOMENDADA:

1. Calcular tasa éxito por mes:
   ae.calcular_tasa_proporciones(df_perfil_cliente, 'contact_month')

2. Identificar "ventanas de oportunidad" temporales
3. Concentrar esfuerzo comercial en meses óptimos
4. Crear calendario de campañas basado en datos

==========================================================
INSIGHT 9: NÚMERO DE CONTACTOS (campaign)
==========================================================

HIPÓTESIS DE LEY DE RENDIMIENTOS DECRECIENTES:
A mayor número de contactos en la misma campaña (campaign):

- Primera llamada: Tasa conversión X%
- Segunda llamada: Tasa conversión X/2
- Tercera llamada+: Tasa conversión marginal

FENÓMENO: "Fatiga de campaña"
Clientes contactados múltiples veces sin éxito:

- Desarrollan resistencia a la oferta
- Percepción negativa ("spam telefónico")
- Menor probabilidad de conversión futura

ACCIÓN RECOMENDADA:

1. Analizar distribución de campaign:
   df_perfil_cliente.groupby('campaign')['y'].mean()

2. Establecer "tope de contactos óptimo" (ej: 3 intentos máximo)
3. Implementar estrategia "Call limiting":

   - Si campaign > 3 y y=0 → Mover a canal alternativo (email)
   - Evitar saturación del cliente

4. Crear regla de negocio:
   if campaign >= 3 and previous_contact == 0:
   priority = "LOW" # Baja prioridad en próximas campañas

==========================================================
INSIGHT 10: PERFIL DEL CLIENTE IDEAL (SÍNTESIS)
==========================================================

CARACTERÍSTICAS DEL CLIENTE CON MAYOR PROPENSIÓN A CONTRATAR:

PERFIL DEMOGRÁFICO:

- Antigüedad con banco: 3-4 años (relativamente reciente)
- Ingreso: Irrelevante (puede ser cualquier nivel)
- Composición hogar: Irrelevante (con/sin hijos)

HISTORIAL COMERCIAL:

- Resultado campaña anterior: "success" (si existe)
- Contactos previos: Nunca contactado o 1-2 intentos máximo
- Bandera previous_contact: Idealmente = 1 (ya fue cliente)

CONTEXTO ECONÓMICO:

- Indicadores macroeconómicos favorables (verificar correlación con y)
- Euribor bajo/estable (momento propicio para ahorrar)

TIMING:

- Mes de contacto: Junio/Julio o Diciembre (pagas extras)
- No contactar en agosto (vacaciones)

VARIABLES A EXCLUIR DEL PERFIL:

- Income (no discrimina)
- Kidhome/Teenhome (no discrimina)
- Duration (data leakage)

SCORE SIMPLIFICADO PROPUESTO (para priorización manual):
SCORE = (antiguedad_dias < 1095) _ 3 # 3 puntos si < 3 años + (poutcome == "success") _ 5 # 5 puntos si éxito previo + (campaign <= 2) _ 2 # 2 puntos si pocos contactos + (contact_month in [6,7,12]) _ 1 # 1 punto mes favorable

Clientes con SCORE >= 7 → Prioridad ALTA
Clientes con SCORE 4-6 → Prioridad MEDIA
Clientes con SCORE < 4 → Prioridad BAJA
