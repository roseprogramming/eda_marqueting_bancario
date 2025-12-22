
# Lista de funciones exportadas por el módulo para importación controlada
__all__ = [
    'plot_numeric_distribution',
    'plot_categorical_rate',
    'plot_correlation_heatmap',
    'plot_boxplot_by_target',
    'save_plot',
    'plot_numeric_comparison_by_target'
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

import pandas as pd  # Para manejo de DataFrames
import numpy as np   # Para operaciones numéricas
import matplotlib.pyplot as plt  # Para gráficos
import seaborn as sns  # Para gráficos estadísticos avanzados
from pathlib import Path  # Para manipulación de rutas de archivos


# Configuración global de estilo para todos los gráficos del proyecto
plt.style.use('seaborn-v0_8-darkgrid')  # Estilo visual de fondo y grillas
sns.set_palette("husl")  # Paleta de colores para consistencia visual


# =============================================================================
# FUNCIONES DE VISUALIZACIÓN
# =============================================================================

def plot_numeric_distribution(df, column, title=None, figsize=(10, 6), bins=30, color='steelblue'):
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


def plot_categorical_rate(df, category_col, target_col, title=None, figsize=(12, 6), 
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
    tasas = df_temp.groupby(category_col).agg(
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
    ax.set_title(title or f'Tasa de Suscripción por {category_col.replace('_', ' ').title()}', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    # Devuelve la figura y el eje si se crearon aquí, o solo el eje si se pasó externo
    if created_fig:
        return fig, ax
    else:
        return None, ax


def plot_correlation_heatmap(df, title=None, figsize=(12, 10), cmap='coolwarm', 
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


def plot_boxplot_by_target(df, numeric_col, target_col, title=None, figsize=(8, 6), palette='rocket'):
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
    ax.set_title(title or f'Distribución de {numeric_col.replace('_', ' ').title()} vs. Suscripción', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Devuelve la figura y el eje
    return fig, ax


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def plot_numeric_comparison_by_target(df, variables, target_col, nombres_graficos, colores, bins=30, figsize=(14, 5)):
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
    import matplotlib.pyplot as plt  # Importación local para evitar conflictos si se usa fuera de notebooks
    for var in variables:
        if var in df.columns:
            # Crea una figura con dos subplots (uno para y=0 y otro para y=1)
            fig, axes = plt.subplots(1, 2, figsize=figsize)
            for i, y_val in enumerate([0, 1]):
                # Filtra los datos según el valor del target y elimina nulos
                data = df[df[target_col] == y_val][var].dropna()
                # Dibuja el histograma para el grupo correspondiente
                axes[i].hist(
                    data,
                    bins=bins,
                    alpha=0.7,
                    edgecolor='black',
                    density=True,
                    label=f'Histograma y={y_val}',
                    color=colores[var][i]
                )
                # Si hay datos, dibuja la KDE y la línea de media
                if not data.empty:
                    data.plot.kde(ax=axes[i], color='darkred', linewidth=2, label='KDE')
                    mean = data.mean()
                    axes[i].axvline(mean, color='green', linestyle='--', linewidth=2, label=f'Media: {mean:.2f}')
                # Configura etiquetas y título de cada subplot
                axes[i].set_xlabel(var, fontsize=12)
                axes[i].set_ylabel('Densidad', fontsize=12)
                axes[i].set_title(f'{var} (y={y_val})', fontsize=13, fontweight='bold')
                axes[i].legend()
                axes[i].grid(axis='y', alpha=0.3)
            # Ajusta el layout para que no se solapen los subplots
            plt.tight_layout()
            # Guarda el gráfico usando la función auxiliar
            save_plot(nombres_graficos[var])
            # Muestra el gráfico en pantalla
            plt.show()

def save_plot(filename, dpi=300, bbox_inches='tight'):
    """
    Guarda la figura actual de matplotlib en la carpeta reports/outputs/ del proyecto.
    Crea la carpeta si no existe y muestra la ruta final por consola.

    Parámetros:
        filename (str): Nombre del archivo (ej: 'grafico.png').
        dpi (int): Resolución del gráfico.
        bbox_inches (str): Ajuste de bordes ('tight' recomendado).

    Detalles:
        - Crea la subcarpeta 'outputs' dentro de 'reports' si no existe.
        - Guarda el archivo y muestra la ruta completa.
    """
    import os
    os.makedirs('reports/outputs', exist_ok=True)
    filepath = f'reports/outputs/{filename}'
    plt.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)
    print(f"✓ Gráfico guardado: {filepath}")
