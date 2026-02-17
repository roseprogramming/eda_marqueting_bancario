
# src/reporte_pdf.py
# ======================================================
# Herramientas para la generación de reportes ejecutivos en PDF.
#
# Este módulo permite consolidar los resultados del análisis EDA en un documento
# PDF profesional, integrando texto explicativo y visualizaciones automáticas.
# Utiliza la librería fpdf2 para mantener una arquitectura de "Python puro".
# ======================================================

from fpdf import FPDF
from datetime import datetime
import os
import pandas as pd
from typing import Dict, List, Optional

def find_project_root(current_path: Optional[str] = None) -> str:
    """Busca la raíz del proyecto. Prioriza la ubicación de este archivo."""
    # Como este archivo está en 'src/', la raíz siempre es el padre de 'src'
    try:
        source_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.basename(source_dir) == 'src':
            return os.path.dirname(source_dir)
    except NameError:
        pass # __file__ no definido en algunos REPLs
    
    if current_path is None:
        current_path = os.getcwd()
    
    # Fallback: búsqueda recursiva
    if os.path.exists(os.path.join(current_path, "venv")) or os.path.exists(os.path.join(current_path, ".git")):
        return current_path
        
    parent = os.path.dirname(current_path)
    if parent == current_path:
        return current_path
        
    return find_project_root(parent)

class ReportePDF(FPDF):
    """
    Clase personalizada para la generación de reportes técnicos del proyecto.
    Hereda de FPDF para extender funcionalidades de encabezado, pie de página y estilos.
    """
    
    def header(self):
        """Configura el encabezado de todas las páginas."""
        # Logo o Título en el encabezado
        self.set_font('helvetica', 'B', 15)
        # Título centrado
        self.cell(0, 10, 'Informe Ejecutivo: EDA Marketing Bancario', border=False, align='C', new_x="LMARGIN", new_y="NEXT")
        # Línea decorativa
        self.set_draw_color(44, 62, 80)  # Azul oscuro profesional
        self.line(10, 22, 200, 22)
        self.ln(10)

    def footer(self):
        """Configura el pie de página de todas las páginas."""
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        # Fecha de generación a la izquierda
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.cell(0, 10, f'Generado el: {fecha}', align='L')
        # Número de página a la derecha
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', align='R')

    def chapter_title(self, label: str):
        """Añade un título de sección con formato consistente."""
        self.set_font('helvetica', 'B', 14)
        self.set_fill_color(240, 240, 240)  # Gris muy claro
        self.set_text_color(44, 62, 80)     # Azul oscuro
        self.cell(0, 10, label, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def add_metric_text(self, text: str):
        """Añade texto explicativo con formato estándar."""
        self.set_font('helvetica', '', 11)
        self.set_text_color(0)
        self.multi_cell(0, 7, text)
        self.ln(2)

    def add_chart(self, image_path: str, width: int = 170):
        """Inserta una imagen (gráfico) centrada si el archivo existe."""
        # Resolver ruta relativa a la raíz del proyecto
        root = find_project_root()
        full_path = os.path.abspath(os.path.join(root, image_path))
        
        if os.path.exists(full_path):
            # Centrar la imagen (página A4 tiene ~210mm de ancho)
            x_pos = (210 - width) / 2
            self.image(full_path, x=x_pos, w=width)
            self.ln(10)
        else:
            self.set_text_color(255, 0, 0)
            self.cell(0, 10, f"[Aviso: Gráfico no encontrado en {image_path}]", new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(0)
            self.ln(5)

def generar_reporte_pdf(tasas_por_variable: Dict, output_path: str = "reports/outputs/informe_ejecutivo_eda.pdf") -> str:
    """
    Función principal que orquesta la creación del PDF integrando datos y gráficos.
    
    Parámetros:
        tasas_por_variable (Dict): Diccionario con los resultados acumulados del EDA.
        output_path (str): Ruta donde se guardará el archivo PDF generado.
        
    Retorna:
        str: Ruta absoluta del archivo generado satisfactoriamente.
    """
    # Asegurar que la ruta de salida es absoluta respecto a la raíz si es relativa
    if not os.path.isabs(output_path):
        root = find_project_root()
        output_path = os.path.join(root, output_path)

    pdf = ReportePDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    
    # ---------------------------------------------------------
    # INTRODUCCIÓN Y RESUMEN
    # ---------------------------------------------------------
    pdf.chapter_title("1. Resumen General del Análisis")
    pdf.add_metric_text(
        "Este informe consolida los hallazgos clave obtenidos durante el Análisis Exploratorio "
        "de Datos (EDA) del proyecto de Marketing Bancario. Se han analizado variables "
        "demográficas, temporales y factores de campaña para identificar patrones que "
        "influyen en la conversión (suscripción de depósitos)."
    )
    
    # Hallazgos clave cuantitativos
    total_vars = len(tasas_por_variable)
    pdf.add_metric_text(f"- Total de variables analizadas: {total_vars}")
    
    # ---------------------------------------------------------
    # SECCIÓN 1: ANÁLISIS TEMPORAL
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.chapter_title("2. Patrones Temporales y Estacionales")
    pdf.add_metric_text(
        "Se analiza la evolución de la tasa de éxito a lo largo del tiempo para detectar "
        "estacionalidad u otros efectos temporales en la captación de clientes."
    )
    
    # Gráfico 03: Registros y Tasa por Periodo
    pdf.add_chart("reports/outputs/03_temporal_registros_tasa_periodo.png")
    
    if 'temporal_mes' in tasas_por_variable:
        data = tasas_por_variable['temporal_mes']
        tasas_mes = pd.Series(data['tasa_exito_por_mes'])
        pdf.add_metric_text(
            f"El análisis por mes revela que el pico de conversión se sitúa en {tasas_mes.idxmax()}, "
            f"con una tasa de {tasas_mes.max():.1f}%, mientras que el mínimo ocurre en {tasas_mes.idxmin()}."
        )

    # Gráfico 04: Mes de contacto
    pdf.add_chart("reports/outputs/04_temporal_registros_tasa_contact_month.png")

    # ---------------------------------------------------------
    # SECCIÓN 2: VARIABLES DEMOGRÁFICAS/NUMÉRICAS
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.chapter_title("3. Comparativa de Variables Numéricas")
    pdf.add_metric_text(
        "Se comparan las distribuciones de variables clave (Edad, Ingresos, Antigüedad) "
        "entre el grupo que contrató el depósito (y=1) y el que no (y=0)."
    )
    
    # Gráfico 06: Histograma Age
    pdf.add_chart("reports/outputs/06_hist_age_comparativo.png", width=160)
    
    if 'age' in tasas_por_variable:
        comp = tasas_por_variable['age']['comparativa']
        pdf.add_metric_text(
            f"En cuanto a la EDAD, el ratio de medias es de {comp['ratio']:.2f}x. "
            "Esto sugiere una diferencia marginal entre los grupos de edad analizados."
        )

    # Gráfico 07: Histograma Income
    pdf.add_chart("reports/outputs/07_hist_income_comparativo.png", width=160)
    
    # ---------------------------------------------------------
    # SECCIÓN 3: VARIABLES CATEGÓRICAS (EL GRAN DIFERENCIADOR)
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.chapter_title("4. Impacto de Variables Categóricas")
    pdf.add_metric_text(
        "Las variables categóricas, como la ocupación y el segmento de edad, han demostrado "
        "ser los factores con mayor poder discriminatorio para el éxito de la campaña."
    )
    
    # Gráfico 09: Tasas categóricas lado a lado
    pdf.add_chart("reports/outputs/09_tasas_exito_categoricas_lado_a_lado.png", width=180)
    
    if 'job' in tasas_por_variable:
        df_job = pd.DataFrame(tasas_por_variable['job']['tabla'])
        top_job = df_job.sort_values('tasa_exito', ascending=False).iloc[0]
        pdf.add_metric_text(
            f"Destaca el segmento de '{top_job.name}' con una tasa de éxito del {top_job['tasa_exito']:.1f}%, "
            "muy por encima de la media global."
        )

    # ---------------------------------------------------------
    # SECCIÓN 4: FACTORES ESTRATÉGICOS (MACRO Y CAMPAÑA)
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.chapter_title("5. Indicadores Macroeconómicos y Especiales")
    
    # Gráfico 11: Variables Macro
    pdf.add_chart("reports/outputs/11_variables_macroeconomicas_conversion.png", width=170)
    
    # Gráfico 12: Factores campaña (Duration y Poutcome)
    pdf.ln(5)
    pdf.chapter_title("6. Factores Críticos de Campaña (Leakage)")
    pdf.add_chart("reports/outputs/12_factores_campana_duracion_vs_poutcome.png", width=170)
    
    pdf.add_metric_text(
        "IMPORTANTE: Se confirma un 'data leakage' crítico en la variable DURACIÓN, "
        "ya que las llamadas exitosas duran significativamente más (ratio 2.5x), "
        "siendo esta una información solo disponible a posteriori."
    )

    # ---------------------------------------------------------
    # GUARDADO FINAL
    # ---------------------------------------------------------
    # Asegurar que el directorio de salida existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    pdf.output(output_path)
    return os.path.abspath(output_path)

if __name__ == "__main__":
    # Prueba rápida si se ejecuta solo (con diccionario vacío o nulo)
    print("Iniciando prueba de generación de PDF...")
    try:
        ruta = generar_reporte_pdf({}, "reports/outputs/test_informe.pdf")
        print(f"Prueba completada con éxito. Archivo en: {ruta}")
    except Exception as e:
        print(f"Error en la prueba: {e}")
