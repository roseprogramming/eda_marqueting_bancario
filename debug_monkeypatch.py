
import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# MONKEY PATCH: Override plt.show to prevent blocking
def non_blocking_show():
    print(" [DEBUG] plt.show() called! Skipping to avoid hang.")
plt.show = non_blocking_show

# Add project root to path
project_root = os.getcwd()
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    import src.analisis_exploratorio as ae
    import src.plotting as pl
except ImportError:
    pass

print("Loading data...")
try:
    df = pd.read_csv('data/processed/df_perfil_cliente.csv', index_col=0)
    print(f"Data shape: {df.shape}")
except FileNotFoundError:
    print("Data file not found.")
    sys.exit(1)

# Prepare data
vars_numericas = [col for col in df.select_dtypes(include=['number']).columns if col != 'y']
nulos_plot = df.isnull().mean() * 100
nulos_plot = nulos_plot[nulos_plot > 0]
vars_con_outliers = [var for var in vars_numericas if ae.hay_outliers(df[var])]

print("Running graficar_nulos_outliers with monkeypatched plt.show...")
pl.graficar_nulos_outliers(df, nulos_plot, vars_con_outliers)
print("Function graficar_nulos_outliers finished successfully!")
