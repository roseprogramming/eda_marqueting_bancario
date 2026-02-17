
# Lista de funciones exportadas por el módulo para importación controlada
__all__ = [
    'graficar_distribucion_numerica',
    'graficar_tasa_categorica',
    'graficar_mapa_correlacion',
    'graficar_boxplot_por_target',
    'guardar_grafico',
    'graficar_comparacion_numerica',
    'graficar_nulos_outliers',
    'graficar_tendencias_temporales'
]

"""
Módulo: plotting.py
======================================================
Funciones de visualización centralizadas para el análisis exploratorio de datos (EDA)
del proyecto de marketing bancario.

Este módulo proporciona funciones reutilizables para la generación de gráficos estadísticos,
comparativos y de correlación, facilitando la exploración visual y la documentación de resultados.

Uso recomendado en notebooks:
    import src.plotting as pl

    # Histograma y KDE de una variable numérica
    fig, ax = pl.plot_numeric_distribution(df, 'age', title='Distribución de Edad')
    plt.show()

    # Tasa de conversión por categoría
    fig, ax = pl.plot_categorical_rate(df, 'job', 'y', title='Tasa por Ocupación')
    plt.show()

    # Mapa de calor de correlaciones
    fig, ax = pl.plot_correlation_heatmap(df_numeric, title='Matriz de Correlación')
    plt.show()

    # Comparativo de variables numéricas por target (genera y guarda varios gráficos)
    pl.plot_numeric_comparison_by_target(df, variables, 'y', nombres_graficos, colores)

    # Guardar cualquier gráfico actual
    pl.save_plot('nombre_archivo.png')

Características:
- Todas las funciones están documentadas y pensadas para uso interactivo en notebooks.
- Los gráficos se guardan automáticamente en la carpeta reports/outputs/ para trazabilidad.
- El módulo está alineado con la estructura y convenciones del proyecto EDA_Marketing_Bancario.
"""


# Importación de librerías principales para visualización y manipulación de datos

# pyre-ignore[21]: Could not find module `pandas`
# pyre-ignore[21]: Could not find module `numpy`
# pyre-ignore[21]: Could not find module `matplotlib.pyplot`
# pyre-ignore[21]: Could not find module `seaborn`
import pandas as pd  # Para manejo de DataFrames
import numpy as np   # Para operaciones numéricas
import matplotlib.pyplot as plt  # Para gráficos
import seaborn as sns  # Para gráficos estadísticos avanzados
from pathlib import Path  # Para manipulación de rutas de archivos
from typing import Any


# Configuración global de estilo para todos los gráficos del proyecto
plt.style.use('seaborn-v0_8-darkgrid')  # Estilo visual de fondo y grillas
sns.set_palette("husl")  # Paleta de colores para consistencia visual


# =============================================================================
# FUNCIONES DE VISUALIZACIÓN
# =============================================================================

def graficar_distribucion_numerica(df: Any, column: Any, title=None, figsize=(10, 6), bins=30, color='steelblue'):
    """
    Dibuja un histograma con KDE y línea de media para una variable numérica.
    Útil para analizar la distribución y detectar sesgos, outliers o asimetrías.

    Parámetros:
        df (pd.DataFrame): DataFrame fuente de datos.
        column (str): Nombre de la columna numérica a graficar.
        title (str, opcional): Título del gráfico.
        figsize (tuple): Tamaño de la figura (ancho, alto).
        bins (int): Número de bins para el histograma.
        color (str): Color de las barras del histograma.

    Retorna:
        fig, ax: Objetos matplotlib de la figura y los ejes.
    """
    # Crea una figura y un eje para el gráfico, con el tamaño especificado
    fig, ax = plt.subplots(figsize=figsize)
    
    # Elimina valores nulos de la columna seleccionada para evitar errores en el gráfico
    data = df[column].dropna()
    
    # Dibuja el histograma de la variable numérica sobre el eje ax
    ax.hist(
        data,  # datos a graficar
        bins=bins,  # número de barras
        color=color,  # color de las barras
        alpha=0.7,  # transparencia
        edgecolor='black',  # color del borde de las barras
        density=True,  # normaliza para mostrar densidad
        label='Histograma'  # etiqueta para la leyenda
    )
    
    # Dibuja la curva de densidad (KDE) sobre el mismo eje
    data.plot.kde(
        ax=ax,  # eje donde dibujar
        color='darkred',  # color de la línea
        linewidth=2,  # grosor de la línea
        label='KDE'  # etiqueta para la leyenda
    )
    
    # Calcula la media de la variable y dibuja una línea vertical en esa posición
    mean_val = data.mean()
    ax.axvline(
        mean_val,  # valor de la media
        color='green',  # color de la línea
        linestyle='--',  # línea discontinua
        linewidth=2,  # grosor
        label=f'Media: {mean_val:.2f}'  # etiqueta para la leyenda
    )
    
    # Configura las etiquetas y el título del gráfico
    ax.set_xlabel(column.replace('_', ' ').title(), fontsize=12)  # Etiqueta eje X
    ax.set_ylabel('Densidad', fontsize=12)  # Etiqueta eje Y
    ax.set_title(title or f'Distribución de {column.replace("_", " ").title()}', fontsize=14, fontweight='bold')  # Título
    ax.legend()  # Muestra la leyenda
    ax.grid(axis='y', alpha=0.3)  # Cuadrícula horizontal
    
    # Devuelve la figura y el eje para uso posterior
    return fig, ax


def graficar_tasa_categorica(df: Any, category_col: Any, target_col: Any, title=None, figsize=(12, 6), 
                          top_n=None, rotation=45, *, color_palette='viridis', ax=None):
    """
    Dibuja un gráfico de barras con la tasa de conversión (porcentaje de éxito) para cada categoría de una variable categórica.
    Ideal para comparar el comportamiento de grupos (ej: ocupación, educación) respecto al target binario.

    Parámetros:
        df (pd.DataFrame): DataFrame fuente de datos.
        category_col (str): Columna categórica a analizar.
        target_col (str): Variable objetivo binaria (0/1 o sí/no).
        title (str, opcional): Título del gráfico.
        figsize (tuple): Tamaño de la figura.
        top_n (int, opcional): Mostrar solo las N categorías con mayor tasa.
        rotation (int): Rotación de etiquetas del eje X.
        color_palette (str): Paleta de colores de seaborn.
        ax (matplotlib.axes.Axes, opcional): Eje sobre el que dibujar (útil para subplots).

    Retorna:
        fig, ax: Figura y ejes del gráfico (si se crea fig), o (None, ax) si se pasa ax externo.
    """
    # Crea un DataFrame temporal solo con las columnas relevantes
    df_temp = df[[category_col, target_col]].copy()
    # Elimina filas con valores nulos para evitar errores
    df_temp = df_temp.dropna()
    
    # Agrupa por la categoría y calcula el total y éxitos (suma del target)
    tasas = df_temp.groupby(category_col, observed=True).agg(
        total=(target_col, 'count'),  # total de registros por categoría
        exitos=(target_col, 'sum')    # suma de éxitos (asume target binario 0/1)
    )
    # Calcula la tasa de éxito como porcentaje
    tasas['tasa_exito'] = (tasas['exitos'] / tasas['total']) * 100
    # Ordena las categorías de mayor a menor tasa
    tasas = tasas.sort_values('tasa_exito', ascending=False)
    
    # Si se especifica top_n, filtra solo las N mejores categorías
    if top_n:
        tasas = tasas.head(top_n)
    
    # Si no se pasa un eje externo, crea una nueva figura y eje
    created_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
        created_fig = True
    else:
        fig = ax.figure  # Usa la figura del eje externo
    # Genera una paleta de colores para las barras
    colors = sns.color_palette(color_palette, len(tasas))
    # Dibuja las barras de la tasa de éxito por categoría
    bars = ax.bar(
        range(len(tasas)),  # posición de cada barra
        tasas['tasa_exito'],  # altura de cada barra
        color=colors,  # colores
        edgecolor='black',  # borde negro
        alpha=0.8  # transparencia
    )
    # Calcula la tasa global de éxito en todo el DataFrame
    tasa_global = (df[target_col].sum() / len(df)) * 100
    # Dibuja una línea horizontal con la tasa global
    ax.axhline(
        tasa_global,
        color='red', linestyle='--', linewidth=2,
        label=f'Tasa Global: {tasa_global:.1f}%'
    )
    # Añade etiquetas de porcentaje encima de cada barra
    for i, (idx, row) in enumerate(tasas.iterrows()):
        ax.text(
            i, row['tasa_exito'] + 0.5, f"{row['tasa_exito']:.1f}%",
            ha='center', fontsize=9, fontweight='bold'
        )
    # Configura los ejes y el título
    ax.set_xticks(range(len(tasas)))
    ax.set_xticklabels(tasas.index, rotation=rotation, ha='right')
    ax.set_xlabel(category_col.replace('_', ' ').title(), fontsize=12)
    ax.set_ylabel('Tasa de Conversión (%)', fontsize=12)
    ax.set_title(title or f"Tasa de Suscripción por {category_col.replace('_', ' ').title()}", fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    # Devuelve la figura y el eje si se crearon aquí, o solo el eje si se pasó externo
    if created_fig:
        return fig, ax
    else:
        return None, ax


def graficar_mapa_correlacion(df: Any, title=None, figsize=(12, 10), cmap='coolwarm', 
                             annot=True, fmt='.2f', vmin=-1, vmax=1):
    """
    Dibuja un mapa de calor (heatmap) de la matriz de correlación entre variables numéricas.
    Permite identificar relaciones fuertes, redundancias y posibles riesgos de multicolinealidad.

    Parámetros:
        df (pd.DataFrame): DataFrame con variables numéricas.
        title (str, opcional): Título del gráfico.
        figsize (tuple): Tamaño de la figura.
        cmap (str): Mapa de colores.
        annot (bool): Mostrar valores numéricos en las celdas.
        fmt (str): Formato de los valores anotados.
        vmin, vmax (float): Rango de valores del color.

    Retorna:
        fig, ax: Figura y ejes del gráfico.
    """
    # Crea una figura y un eje para el heatmap
    fig, ax = plt.subplots(figsize=figsize)
    
    # Calcula la matriz de correlación entre todas las columnas numéricas
    corr_matrix = df.corr()
    
    # Dibuja el mapa de calor de la matriz de correlación
    sns.heatmap(
        corr_matrix,  # matriz de correlación
        annot=annot,  # muestra los valores numéricos
        fmt=fmt,  # formato de los valores
        cmap=cmap,  # mapa de colores
        vmin=vmin, vmax=vmax,  # rango de colores
        square=True,  # celdas cuadradas
        linewidths=0.5,  # grosor de líneas entre celdas
        cbar_kws={"shrink": 0.8},  # tamaño de la barra de color
        ax=ax  # eje donde dibujar
    )
    
    # Configura el título del gráfico
    ax.set_title(title or 'Matriz de Correlación entre Variables Numéricas', fontsize=14, fontweight='bold', pad=20)
    
    # Rota las etiquetas de los ejes para mejor visualización
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # Devuelve la figura y el eje
    return fig, ax


def graficar_boxplot_por_target(df: Any, numeric_col: Any, target_col: Any, title=None, figsize=(8, 6), palette='rocket'):
    """
    Dibuja un boxplot para comparar la distribución de una variable numérica según el valor del target.
    Útil para visualizar diferencias de dispersión, mediana y outliers entre grupos (ej: y=0 vs y=1).

    Parámetros:
        df (pd.DataFrame): DataFrame fuente de datos.
        numeric_col (str): Columna numérica a analizar.
        target_col (str): Variable objetivo binaria.
        title (str, opcional): Título del gráfico.
        figsize (tuple): Tamaño de la figura.
        palette (str): Paleta de colores para los grupos.

    Retorna:
        fig, ax: Figura y ejes del gráfico.
    """
    # Crea una figura y un eje para el boxplot
    fig, ax = plt.subplots(figsize=figsize)
    
    # Dibuja el boxplot comparando la variable numérica según el target
    sns.boxplot(
        x=target_col,  # variable categórica (target)
        y=numeric_col,  # variable numérica
        data=df,  # datos
        palette=palette,  # paleta de colores
        ax=ax,  # eje donde dibujar
        hue=target_col,  # colorea por grupo
        legend=False  # no muestra leyenda automática
    )
    
    # Configura etiquetas y título
    ax.set_xlabel(f'{target_col} (0=No, 1=Sí)', fontsize=12)
    ax.set_ylabel(numeric_col.replace('_', ' ').title(), fontsize=12)
    ax.set_title(title or f"Distribución de {numeric_col.replace('_', ' ').title()} vs. Suscripción", fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Devuelve la figura y el eje
    return fig, ax


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def graficar_nulos_outliers(df: Any, nulos_plot: Any, vars_con_outliers: Any):
    """
    Visualiza el porcentaje de valores nulos y los outliers de variables numéricas en un DataFrame.
    Genera una figura con dos subplots:
        (1) Barplot horizontal de porcentaje de nulos por variable (solo variables con nulos)
        (2) Boxplots de variables numéricas con outliers detectados

    Debe recibirse desde el notebook:
        - df (pd.DataFrame): DataFrame fuente de datos (para graficar boxplots)
        - nulos_plot (pd.Series): Porcentaje de nulos por variable (solo variables con nulos)
        - vars_con_outliers (list of str): Lista de variables numéricas con outliers detectados
        - figsize (tuple, opcional): Tamaño de la figura.

    Ejemplo de uso en notebook:
        porcentaje_nulos = df.isnull().mean().sort_values(ascending=False) * 100
        nulos_plot = porcentaje_nulos[porcentaje_nulos > 0].sort_values()
        vars_con_outliers = [var for var in vars_numericas if hay_outliers(df[var])]
        pl.plot_nulls_and_outliers(df, nulos_plot, vars_con_outliers)
    """
    # -------------------------------------------------------------------------
    # Configuración de la figura y subplots
    # -------------------------------------------------------------------------
    n_nulos = max(1, len(nulos_plot))  # Número de variables con nulos (mínimo 1)
    n_out = max(1, len(vars_con_outliers))  # Número de variables con outliers (mínimo 1)
    fig_width = max(8, int(2.5 * max(n_nulos, n_out)))  # Ancho dinámico
    subplot_height = 6  # Altura fija por subplot
    fig, axes = plt.subplots(2, 1, figsize=(fig_width, subplot_height*2), gridspec_kw={'height_ratios': [1, 1]})  # Dos subplots verticales

    # -------------------------------------------------------------------------
    # Subplot 1: Barplot horizontal de porcentaje de nulos
    # -------------------------------------------------------------------------
    if len(nulos_plot) > 0:
        nulos_df = nulos_plot.reset_index()  # Convierte el Series en DataFrame para graficar
        nulos_df['Variable'] = nulos_df['index']  # Renombra la columna de índice a 'Variable'
        nulos_df['hue'] = nulos_df['index']  # Crea una columna para asignar un color único a cada variable
        color_palette_nulos = sns.color_palette("pastel", len(nulos_df))  # Paleta de colores pastel para las barras
        # Dibuja el barplot horizontal de porcentaje de nulos
        sns.barplot(y="Variable", x=0, data=nulos_df, hue="hue", dodge=False, palette=color_palette_nulos, ax=axes[0], legend=False)
        axes[0].set_xlabel('% de nulos')  # Etiqueta del eje X
        axes[0].set_ylabel('Variable')  # Etiqueta del eje Y
        axes[0].set_title('Porcentaje de valores nulos por variable (>0%)')  # Título del gráfico
    else:
        axes[0].text(0.5, 0.5, 'No hay valores nulos', ha='center', va='center', fontsize=12)  # Mensaje si no hay nulos
        axes[0].set_axis_off()  # Oculta el subplot si no hay nulos

    # ------------------------------------------------------------------------- 
    # Subplot 2: Boxplots de variables numéricas con outliers
    # -------------------------------------------------------------------------
    if vars_con_outliers:
        df_long = df[vars_con_outliers].melt(var_name='Variable', value_name='Valor')  # Convierte a formato largo para boxplot
        df_long['hue'] = df_long['Variable']  # Crea columna para color único por variable
        color_palette = sns.color_palette("pastel", len(vars_con_outliers))  # Paleta pastel para boxplots
        # Dibuja los boxplots de cada variable con outliers
        sns.boxplot(x='Variable', y='Valor', data=df_long, hue='hue', dodge=False, palette=color_palette, ax=axes[1], order=vars_con_outliers, legend=False)
        axes[1].set_xlabel('Variable')  # Etiqueta eje X
        axes[1].set_ylabel('Valor')  # Etiqueta eje Y
        axes[1].set_title('Boxplots de variables numéricas con outliers detectados')  # Título del gráfico
        if len(vars_con_outliers) > 8:
            axes[1].tick_params(axis='x', rotation=45)  # Rota etiquetas si hay muchas variables
    else:
        axes[1].text(0.5, 0.5, 'No se detectaron outliers en las variables numéricas.', ha='center', va='center', fontsize=12)  # Mensaje si no hay outliers
        axes[1].set_axis_off()  # Oculta el subplot si no hay outliers

    plt.tight_layout()  # Ajusta el layout para evitar solapamientos
    return fig, axes
    # -------------------------------------------------------------------------

def graficar_comparacion_numerica(df: Any, variables: Any, target_col: Any, nombres_graficos: Any, colores: Any, bins=30, figsize=(14, 5)):
    """
    Genera gráficos comparativos (histograma + KDE + línea de media) para cada variable numérica,
    separando por el valor del target (ej: y=0 vs y=1). Cada gráfico se guarda automáticamente.

    Parámetros:
        df (pd.DataFrame): DataFrame fuente de datos.
        variables (list of str): Lista de columnas numéricas a graficar.
        target_col (str): Variable objetivo binaria.
        nombres_graficos (dict): Diccionario {variable: nombre_archivo.png} para guardar cada gráfico.
        colores (dict): Diccionario {variable: [color_y0, color_y1]} para los grupos.
        bins (int): Número de bins para el histograma.
        figsize (tuple): Tamaño de la figura (ancho, alto).

    Detalles:
        - Para cada variable, genera dos subgráficos: uno para y=0 y otro para y=1.
        - Incluye histograma, KDE y línea de media en cada subplot.
        - Guarda el gráfico en reports/outputs/ y lo muestra en pantalla.
    """
    # pyre-ignore[21]: Could not find module `matplotlib.pyplot`
    import matplotlib.pyplot as plt  # Importación local para evitar conflictos si se usa fuera de notebooks
    generated_plots = []
    for var in variables:
        if var in df.columns:
            # Crea una figura con dos subplots (uno para y=0 y otro para y=1)
            fig, axes = plt.subplots(1, 2, figsize=figsize)
            for i, y_val in enumerate([0, 1]):
                # Filtra los datos según el valor del target y elimina nulos
                data = df[df[target_col] == y_val][var].dropna()
                # Dibuja el histograma para el grupo correspondiente
                # pyre-ignore[16]: axes is dynamically typed
                # pyre-ignore[24]: Generic type mismatch
                axes[i].hist(
                    data,
                    bins=bins,
                    # pyre-ignore[16]: Item `Any` of `Any` is not an indexable.
                    color=colores[var][i],
                    alpha=0.7,
                    edgecolor='black',
                    density=True,
                    label=f'Histograma y={y_val}'
                )
                # Si hay datos, dibuja la KDE y la línea de media
                if not data.empty:
                    # pyre-ignore[16]: axes likely Any
                    data.plot.kde(ax=axes[i], color='darkred', linewidth=2, label='KDE')
                    mean = data.mean()
                    # pyre-ignore[16]: axes likely Any
                    axes[i].axvline(mean, color='green', linestyle='--', linewidth=2, label=f'Media: {mean:.2f}')
                # Configura etiquetas y título de cada subplot
                # pyre-ignore[16]: axes likely Any
                axes[i].set_xlabel(var, fontsize=12)
                # pyre-ignore[16]: axes likely Any
                axes[i].set_ylabel('Densidad', fontsize=12)
                # pyre-ignore[16]: axes likely Any
                axes[i].set_title(f'{var} (y={y_val})', fontsize=13, fontweight='bold')
                # pyre-ignore[16]: axes likely Any
                axes[i].legend()
                # pyre-ignore[16]: axes likely Any
                axes[i].grid(axis='y', alpha=0.3)
            # Ajusta el layout para que no se solapen los subplots
            plt.tight_layout()
            # Guarda el gráfico usando la función auxiliar
            # pyre-ignore[16]: Item `Any` of `Any` is not an indexable.
            guardar_grafico(nombres_graficos[var])
            generated_plots.append((fig, axes))

    return generated_plots

def guardar_grafico(filename, dpi=300, bbox_inches='tight'):
    """
    Guarda la figura actual de matplotlib en la carpeta reports/outputs/ del proyecto.
    Crea la carpeta si no existe y muestra la ruta final por consola.

    Parámetros:
        filename (str): Nombre del archivo (ej: 'grafico.png').
        dpi (int): Resolución del gráfico.
        bbox_inches (str): Ajuste de bordes ('tight' recomendado).

    Detalles:
        - Busca la raíz del proyecto subiendo directorios hasta encontrar 'reports/'.
        - Crea la subcarpeta 'outputs' si no existe.
        - Guarda el archivo y muestra la ruta completa.
    """
    # Usa las importaciones globales de Path y plt
    # Obtiene la ruta absoluta del archivo actual
    current_path = Path(__file__).resolve()
    # Busca la carpeta 'reports' subiendo en la jerarquía de carpetas
    for parent in current_path.parents:
        if (parent / 'reports').exists():
            outputs_dir = parent / 'reports' / 'outputs'  # Carpeta destino
            outputs_dir.mkdir(parents=True, exist_ok=True)  # Crea la carpeta si no existe
            break
    else:
        # Si no encuentra la carpeta 'reports', lanza un error
        raise FileNotFoundError("No se encontró la carpeta 'reports' en la jerarquía de directorios.")
    # Construye la ruta final del archivo a guardar
    output_path = outputs_dir / filename
    # Guarda la figura actual en la ruta especificada
    plt.savefig(output_path, dpi=dpi, bbox_inches=bbox_inches)
    # Imprime la ruta donde se guardó el gráfico
    print(f"Gráfico guardado en: {output_path}")


def graficar_tendencias_temporales(df: Any, columna_fecha: Any, target_col: Any, nombre_grafico: Any):
    """
    Genera un gráfico dual (barras para volumen, línea para tasa de éxito) 
    para analizar tendencias temporales.

    Parámetros:
        df: DataFrame con los datos
        columna_fecha: Columna con la fecha o periodo (ej: 'contact_month')
        target_col: Variable objetivo (0/1)
        nombre_grafico: Nombre del archivo para guardar
    """
    # pyre-ignore[21]: Could not find module `matplotlib.pyplot`
    import matplotlib.pyplot as plt
    # pyre-ignore[21]: Could not find module `seaborn`
    import seaborn as sns
    
    # Agrupar datos
    temp_df = df.groupby(columna_fecha)[target_col].agg(['count', 'mean']).reset_index()
    temp_df.columns = [columna_fecha, 'volumen', 'tasa_exito']
    temp_df['tasa_exito'] = temp_df['tasa_exito'] * 100

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Gráfico de barras (Volumen)
    sns.barplot(data=temp_df, x=columna_fecha, y='volumen', color='skyblue', alpha=0.6, ax=ax1)
    ax1.set_ylabel('Cantidad de Contactos', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Eje secundario para Tasa de Éxito
    ax2 = ax1.twinx()
    sns.lineplot(data=temp_df, x=columna_fecha, y='tasa_exito', color='red', marker='o', linewidth=2, ax=ax2)
    ax2.set_ylabel('Tasa de Conversión (%)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Línea promedio global
    global_rate = df[target_col].mean() * 100
    ax2.axhline(global_rate, color='green', linestyle='--', label=f'Promedio: {global_rate:.1f}%')
    ax2.legend(loc='upper right')

    plt.title(f'Tendencia Temporal: {columna_fecha}', fontsize=14)
    plt.tight_layout()
    
    # Usar guardar_grafico que ya existe en el módulo
    guardar_grafico(nombre_grafico)
    return fig, ax1
