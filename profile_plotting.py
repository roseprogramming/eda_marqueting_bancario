
import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Non-interactive
import matplotlib.pyplot as plt
import seaborn as sns
import time

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

# Prepare data for plotting
vars_numericas = [col for col in df.select_dtypes(include=['number']).columns if col != 'y']
print(f"Num vars: {len(vars_numericas)}")

nulos_plot = df.isnull().mean() * 100
nulos_plot = nulos_plot[nulos_plot > 0]
print(f"Nulos plot size: {len(nulos_plot)}")
if len(nulos_plot) > 0:
    print(f"Nulos plot index: {nulos_plot.index.tolist()}")

vars_con_outliers = [var for var in vars_numericas if ae.hay_outliers(df[var])]
print(f"Vars with outliers: {len(vars_con_outliers)}")
print(f"Outlier vars: {vars_con_outliers}")

# Calculate figure dimensions exactly as in the function
n_nulos = max(1, len(nulos_plot))
n_out = max(1, len(vars_con_outliers))
fig_width = max(8, int(2.5 * max(n_nulos, n_out)))
print(f"Calculated Fig Width: {fig_width}")

# Check memory for melt
if vars_con_outliers:
    print("Simulating melt...")
    start = time.time()
    df_long = df[vars_con_outliers].melt(var_name='Variable', value_name='Valor')
    print(f"Melt shape: {df_long.shape}")
    print(f"Melt time: {time.time() - start:.2f}s")

print("Attempting to run function with timeout check...")
# We won't run actual function to avoid hang, just simulated the parts.
# actually, let's try running it but we know it might hang.
# The user wants to know WHY.
# If fig_width is reasonable and melt is fast, then it's likely the plotting itself or plt.show()
