"""
Módulo: plotting.py
======================================================
Funciones de visualización para el análisis exploratorio de datos
del proyecto de marketing bancario.

Uso en notebook:
    from src.plotting import plot_numeric_distribution, plot_categorical_rate, plot_correlation_heatmap
    
    # Distribución de edad
    fig, ax = plot_numeric_distribution(df, 'age', title='Distribución de Edad')
    plt.show()
    
    # Tasa de conversión por ocupación
    fig, ax = plot_categorical_rate(df, 'job', 'y', title='Tasa por Ocupación')
    plt.show()
    
    # Correlación entre variables numéricas
    fig, ax = plot_correlation_heatmap(df_numeric, title='Matriz de Correlación')
    plt.show()
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración global de gráficos
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


# =============================================================================
# FUNCIONES DE VISUALIZACIÓN
# =============================================================================

def plot_numeric_distribution(df, column, title=None, figsize=(10, 6), bins=30, color='steelblue'):
    """
    Genera histograma con KDE para variables numéricas.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    column : str
        Nombre de la columna numérica a graficar
    title : str, optional
        Título del gráfico (por defecto: 'Distribución de {column}')
    figsize : tuple
        Tamaño de la figura (ancho, alto)
    bins : int
        Número de bins para el histograma
    color : str
        Color de las barras
        
    Returns:
    --------
    fig, ax : matplotlib objects
        Figura y ejes del gráfico
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Filtrar valores no nulos
    data = df[column].dropna()
    
    # Histograma + KDE
    ax.hist(data, bins=bins, color=color, alpha=0.7, edgecolor='black', density=True, label='Histograma')
    
    # Línea KDE
    data.plot.kde(ax=ax, color='darkred', linewidth=2, label='KDE')
    
    # Línea de media
    mean_val = data.mean()
    ax.axvline(mean_val, color='green', linestyle='--', linewidth=2, label=f'Media: {mean_val:.2f}')
    
    # Etiquetas
    ax.set_xlabel(column.replace('_', ' ').title(), fontsize=12)
    ax.set_ylabel('Densidad', fontsize=12)
    ax.set_title(title or f'Distribución de {column.replace("_", " ").title()}', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    return fig, ax


def plot_categorical_rate(df, category_col, target_col, title=None, figsize=(12, 6), 
                          top_n=None, rotation=45, color_palette='viridis'):
    """
    Genera gráfico de barras con tasa de conversión por categoría.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    category_col : str
        Nombre de la columna categórica (ej: 'job', 'education')
    target_col : str
        Nombre de la variable objetivo binaria (ej: 'y')
    title : str, optional
        Título del gráfico
    figsize : tuple
        Tamaño de la figura
    top_n : int, optional
        Mostrar solo las top N categorías por tasa
    rotation : int
        Rotación de las etiquetas del eje X
    color_palette : str
        Paleta de colores de seaborn
        
    Returns:
    --------
    fig, ax : matplotlib objects
        Figura y ejes del gráfico
    """
    # Calcular tasas por categoría
    df_temp = df[[category_col, target_col]].copy()
    df_temp = df_temp.dropna()
    
    tasas = df_temp.groupby(category_col).agg(
        total=(target_col, 'count'),
        exitos=(target_col, 'sum')
    )
    tasas['tasa_exito'] = (tasas['exitos'] / tasas['total']) * 100
    tasas = tasas.sort_values('tasa_exito', ascending=False)
    
    # Filtrar top_n si se especifica
    if top_n:
        tasas = tasas.head(top_n)
    
    # Crear gráfico
    fig, ax = plt.subplots(figsize=figsize)
    
    # Barras
    colors = sns.color_palette(color_palette, len(tasas))
    bars = ax.bar(range(len(tasas)), tasas['tasa_exito'], color=colors, edgecolor='black', alpha=0.8)
    
    # Línea de tasa global
    tasa_global = (df[target_col].sum() / len(df)) * 100
    ax.axhline(tasa_global, color='red', linestyle='--', linewidth=2, 
               label=f'Tasa Global: {tasa_global:.1f}%')
    
    # Etiquetas en barras
    for i, (idx, row) in enumerate(tasas.iterrows()):
        ax.text(i, row['tasa_exito'] + 0.5, f"{row['tasa_exito']:.1f}%", 
                ha='center', fontsize=9, fontweight='bold')
    
    # Configuración de ejes
    ax.set_xticks(range(len(tasas)))
    ax.set_xticklabels(tasas.index, rotation=rotation, ha='right')
    ax.set_xlabel(category_col.replace('_', ' ').title(), fontsize=12)
    ax.set_ylabel('Tasa de Conversión (%)', fontsize=12)
    ax.set_title(title or f'Tasa de Suscripción por {category_col.replace("_", " ").title()}', 
                 fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    return fig, ax


def plot_correlation_heatmap(df, title=None, figsize=(12, 10), cmap='coolwarm', 
                             annot=True, fmt='.2f', vmin=-1, vmax=1):
    """
    Genera mapa de calor de correlaciones entre variables numéricas.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con variables numéricas
    title : str, optional
        Título del gráfico
    figsize : tuple
        Tamaño de la figura
    cmap : str
        Mapa de colores (coolwarm, RdBu_r, etc.)
    annot : bool
        Mostrar valores de correlación en celdas
    fmt : str
        Formato de los valores anotados
    vmin, vmax : float
        Rango de valores del mapa de color
        
    Returns:
    --------
    fig, ax : matplotlib objects
        Figura y ejes del gráfico
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Calcular matriz de correlación
    corr_matrix = df.corr()
    
    # Crear heatmap
    sns.heatmap(corr_matrix, annot=annot, fmt=fmt, cmap=cmap, 
                vmin=vmin, vmax=vmax, square=True, linewidths=0.5,
                cbar_kws={"shrink": 0.8}, ax=ax)
    
    # Configuración
    ax.set_title(title or 'Matriz de Correlación entre Variables Numéricas', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Rotar etiquetas
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    return fig, ax


def plot_boxplot_by_target(df, numeric_col, target_col, title=None, figsize=(8, 6), palette='rocket'):
    """
    Genera boxplot comparando distribución de variable numérica por valor del target.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    numeric_col : str
        Nombre de la columna numérica
    target_col : str
        Nombre de la variable objetivo binaria
    title : str, optional
        Título del gráfico
    figsize : tuple
        Tamaño de la figura
    palette : str
        Paleta de colores
        
    Returns:
    --------
    fig, ax : matplotlib objects
        Figura y ejes del gráfico
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Boxplot
    sns.boxplot(x=target_col, y=numeric_col, data=df, palette=palette, ax=ax, hue=target_col, legend=False)
    
    # Etiquetas
    ax.set_xlabel(f'{target_col} (0=No, 1=Sí)', fontsize=12)
    ax.set_ylabel(numeric_col.replace('_', ' ').title(), fontsize=12)
    ax.set_title(title or f'Distribución de {numeric_col.replace("_", " ").title()} vs. Suscripción', 
                 fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    return fig, ax


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def save_plot(filename, dpi=300, bbox_inches='tight'):
    """
    Guarda el gráfico actual en la carpeta reports/outputs/
    
    Parameters:
    -----------
    filename : str
        Nombre del archivo (sin ruta)
    dpi : int
        Resolución del gráfico
    bbox_inches : str
        Ajuste de bordes ('tight' para ajustar automáticamente)
    """
    import os
    os.makedirs('reports/outputs', exist_ok=True)
    filepath = f'reports/outputs/{filename}'
    plt.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)
    print(f"✓ Gráfico guardado: {filepath}")
