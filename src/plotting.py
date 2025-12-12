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


def plot_time_series_rate(df, date_col, target_col, freq='M', title=None, figsize=(14, 6)):
    """
    Genera gráfico de serie temporal de tasa de conversión.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    date_col : str
        Nombre de la columna de fecha
    target_col : str
        Nombre de la variable objetivo binaria
    freq : str
        Frecuencia de agregación ('M'=mensual, 'Q'=trimestral, 'Y'=anual)
    title : str, optional
        Título del gráfico
    figsize : tuple
        Tamaño de la figura
        
    Returns:
    --------
    fig, ax : matplotlib objects
        Figura y ejes del gráfico
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Preparar datos
    df_temp = df[[date_col, target_col]].copy()
    df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors='coerce')
    df_temp = df_temp.dropna()
    
    # Agrupar por periodo
    df_temp['period'] = df_temp[date_col].dt.to_period(freq)
    
    # Calcular tasas
    tasas = df_temp.groupby('period').agg(
        total=(target_col, 'count'),
        exitos=(target_col, 'sum')
    )
    tasas['tasa'] = (tasas['exitos'] / tasas['total']) * 100
    
    # Convertir periodo a timestamp para graficar
    tasas.index = tasas.index.to_timestamp()
    
    # Línea principal
    ax.plot(tasas.index, tasas['tasa'], marker='o', linewidth=2, markersize=8, color='steelblue', label='Tasa de Conversión')
    
    # Línea de tasa global
    tasa_global = (df[target_col].sum() / len(df)) * 100
    ax.axhline(tasa_global, color='red', linestyle='--', linewidth=2, label=f'Media Global: {tasa_global:.1f}%')
    
    # Etiquetas en puntos
    for idx, val in zip(tasas.index, tasas['tasa']):
        ax.text(idx, val + 0.5, f"{val:.1f}%", ha='center', fontsize=9)
    
    # Configuración
    ax.set_xlabel('Periodo', fontsize=12)
    ax.set_ylabel('Tasa de Conversión (%)', fontsize=12)
    ax.set_title(title or 'Evolución Temporal de la Tasa de Conversión', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    return fig, ax


def plot_campaign_effectiveness(df, campaign_col, target_col, title=None, figsize=(12, 6), max_campaigns=10):
    """
    Genera gráfico de efectividad por número de contactos.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    campaign_col : str
        Nombre de la columna de número de contactos
    target_col : str
        Nombre de la variable objetivo binaria
    title : str, optional
        Título del gráfico
    figsize : tuple
        Tamaño de la figura
    max_campaigns : int
        Máximo número de campañas a mostrar
        
    Returns:
    --------
    fig, ax : matplotlib objects
        Figura y ejes del gráfico
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Preparar datos
    df_temp = df[[campaign_col, target_col]].copy()
    df_temp = df_temp.dropna()
    df_temp[campaign_col] = df_temp[campaign_col].clip(upper=max_campaigns)
    
    # Calcular estadísticas
    stats = df_temp.groupby(campaign_col).agg(
        total=(target_col, 'count'),
        exitos=(target_col, 'sum')
    )
    stats['tasa'] = (stats['exitos'] / stats['total']) * 100
    
    # Gráfico 1: Tasa de conversión
    colors = ['green' if t > stats['tasa'].mean() else 'orange' for t in stats['tasa']]
    ax1.bar(stats.index, stats['tasa'], color=colors, edgecolor='black', alpha=0.8)
    ax1.axhline(stats['tasa'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {stats["tasa"].mean():.1f}%')
    ax1.set_xlabel('Número de Contactos', fontsize=12)
    ax1.set_ylabel('Tasa de Conversión (%)', fontsize=12)
    ax1.set_title('Tasa de Conversión por Contactos', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Gráfico 2: Volumen de clientes
    ax2.bar(stats.index, stats['total'], color='steelblue', edgecolor='black', alpha=0.8)
    ax2.set_xlabel('Número de Contactos', fontsize=12)
    ax2.set_ylabel('Número de Clientes', fontsize=12)
    ax2.set_title('Volumen de Clientes por Contactos', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Añadir etiquetas
    for i, (idx, row) in enumerate(stats.iterrows()):
        ax1.text(idx, row['tasa'] + 0.5, f"{row['tasa']:.1f}%", ha='center', fontsize=9)
        ax2.text(idx, row['total'] + 100, f"{int(row['total'])}", ha='center', fontsize=9)
    
    fig.suptitle(title or 'Análisis de Efectividad de Campañas', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    return fig, (ax1, ax2)


def plot_segment_analysis(df, segment_col, target_col, title=None, figsize=(14, 6), min_size=100):
    """
    Genera análisis visual de segmentos con tasa y tamaño.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    segment_col : str
        Nombre de la columna de segmentación
    target_col : str
        Nombre de la variable objetivo binaria
    title : str, optional
        Título del gráfico
    figsize : tuple
        Tamaño de la figura
    min_size : int
        Tamaño mínimo de segmento para mostrar
        
    Returns:
    --------
    fig, ax : matplotlib objects
        Figura y ejes del gráfico
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Preparar datos
    df_temp = df[[segment_col, target_col]].copy()
    df_temp = df_temp.dropna()
    
    # Calcular estadísticas
    stats = df_temp.groupby(segment_col, observed=False).agg(
        total=(target_col, 'count'),
        exitos=(target_col, 'sum')
    )
    stats = stats[stats['total'] >= min_size]  # Filtrar segmentos pequeños
    stats['tasa'] = (stats['exitos'] / stats['total']) * 100
    stats = stats.sort_values('tasa', ascending=False)
    
    # Crear gráfico de barras con doble eje
    x_pos = range(len(stats))
    
    # Eje 1: Tasa de conversión
    color1 = 'steelblue'
    ax.bar(x_pos, stats['tasa'], color=color1, alpha=0.8, edgecolor='black', label='Tasa de Conversión (%)')
    ax.set_xlabel(segment_col.replace('_', ' ').title(), fontsize=12)
    ax.set_ylabel('Tasa de Conversión (%)', color=color1, fontsize=12)
    ax.tick_params(axis='y', labelcolor=color1)
    
    # Línea de tasa global
    tasa_global = (df[target_col].sum() / len(df)) * 100
    ax.axhline(tasa_global, color='red', linestyle='--', linewidth=2, label=f'Media: {tasa_global:.1f}%')
    
    # Eje 2: Tamaño del segmento
    ax2 = ax.twinx()
    color2 = 'darkgreen'
    ax2.plot(x_pos, stats['total'], color=color2, marker='D', linewidth=2, markersize=8, label='Tamaño Segmento')
    ax2.set_ylabel('Número de Clientes', color=color2, fontsize=12)
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Configuración
    ax.set_xticks(x_pos)
    ax.set_xticklabels(stats.index, rotation=45, ha='right')
    ax.set_title(title or f'Análisis de Segmentos: {segment_col.replace("_", " ").title()}', fontsize=14, fontweight='bold')
    
    # Leyendas
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    ax.grid(axis='y', alpha=0.3)
    
    return fig, ax


def plot_economic_impact(df, economic_vars, target_col, title=None, figsize=(14, 8), n_bins=5):
    """
    Genera análisis de impacto de variables económicas.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    economic_vars : list
        Lista de nombres de variables económicas
    target_col : str
        Nombre de la variable objetivo binaria
    title : str, optional
        Título del gráfico
    figsize : tuple
        Tamaño de la figura
    n_bins : int
        Número de bins para discretizar variables continuas (default: 5)
        
    Returns:
    --------
    fig, axes : matplotlib objects
        Figura y ejes del gráfico
    """
    n_vars = len(economic_vars)
    n_cols = 2
    n_rows = (n_vars + 1) // 2
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten() if n_vars > 1 else [axes]
    
    for idx, var in enumerate(economic_vars):
        ax = axes[idx]
        
        # Preparar datos
        df_temp = df[[var, target_col]].copy()
        df_temp = df_temp.dropna()
        
        # Crear bins
        df_temp[f'{var}_bin'] = pd.qcut(df_temp[var], q=n_bins, duplicates='drop')
        
        # Calcular tasas por bin
        stats = df_temp.groupby(f'{var}_bin', observed=False).agg(
            total=(target_col, 'count'),
            exitos=(target_col, 'sum')
        )
        stats['tasa'] = (stats['exitos'] / stats['total']) * 100
        
        # Graficar
        x_labels = [f"{interval.left:.2f} - {interval.right:.2f}" for interval in stats.index]
        colors = sns.color_palette("RdYlGn", len(stats))
        ax.bar(range(len(stats)), stats['tasa'], color=colors, edgecolor='black', alpha=0.8)
        
        # Línea de media
        tasa_global = (df[target_col].sum() / len(df)) * 100
        ax.axhline(tasa_global, color='red', linestyle='--', linewidth=2, alpha=0.7)
        
        ax.set_title(f'{var.replace("_", " ").title()}', fontsize=11, fontweight='bold')
        ax.set_xlabel('Rango', fontsize=10)
        ax.set_ylabel('Tasa (%)', fontsize=10)
        ax.set_xticks(range(len(stats)))
        ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8)
        ax.grid(axis='y', alpha=0.3)
    
    # Ocultar ejes extras
    for idx in range(len(economic_vars), len(axes)):
        axes[idx].set_visible(False)
    
    fig.suptitle(title or 'Impacto de Variables Económicas en Conversión', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig, axes
