# -*- coding: utf-8 -*-
"""
Created on Sat May 24 18:24:08 2025

@author: cavus
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ------------------------------
# 1. Load and Prepare Data
# ------------------------------
data_path = r"C:\Users\cavus\Desktop\ICC_Conference\data_for_energyy.csv"
save_path = r"C:\Users\cavus\Desktop\ICC_Conference"

df = pd.read_csv(data_path)
df['time'] = pd.to_datetime(df['time'])
df_24h = df.tail(24).copy()
df_24h.set_index('time', inplace=True)

# ------------------------------
# 2. Define Market and DER Inputs
# ------------------------------
price = df_24h['spot_market_price']
load = df_24h['consumption']
pv = df_24h['pv_production']
wind = df_24h['wind_production']

price_threshold = price.quantile(0.90)
high_price = price > price_threshold

# ------------------------------
# 3. ClimaGrid Adaptive Dispatch
# ------------------------------
battery_capacity = 5.0
fuel_cell_capacity = 10.0
battery_soc = battery_capacity
fuel_cell_energy = fuel_cell_capacity

battery_dispatch = np.zeros_like(load)
fuel_cell_dispatch = np.zeros_like(load)
grid_import = np.zeros_like(load)
renewable_used = np.zeros_like(load)

for i in range(len(load)):
    demand = load.iloc[i]
    renewable = pv.iloc[i] + wind.iloc[i]
    price_now = price.iloc[i]

    use_renewables = min(demand, renewable)
    renewable_used[i] = use_renewables
    remaining = demand - use_renewables

    battery_use = min(battery_soc, remaining, 0.7 if high_price.iloc[i] else 0.4)
    battery_soc -= battery_use
    remaining -= battery_use
    battery_dispatch[i] = battery_use

    fuel_use = min(fuel_cell_energy, remaining, 0.7 if high_price.iloc[i] else 0.4)
    fuel_cell_energy -= fuel_use
    remaining -= fuel_use
    fuel_cell_dispatch[i] = fuel_use

    grid_import[i] = remaining

# ------------------------------
# 4. Figure 5 – DER and Grid Contribution Stackplot
# ------------------------------
plt.figure(figsize=(12, 6), dpi=300)
plt.stackplot(df_24h.index,
              renewable_used,
              battery_dispatch,
              fuel_cell_dispatch,
              grid_import,
              labels=['Renewables', 'Battery', 'Fuel Cell', 'Grid Import'],
              colors=['#a1d99b', '#238b45', '#9e9ac8', '#f03b20'])
plt.title('Figure 5: ClimaGrid DER and Grid Contribution to Demand', fontsize=18)
plt.xlabel('Time', fontsize=16)
plt.ylabel('Power (kW)', fontsize=16)
plt.legend(loc='upper right', fontsize=12)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(save_path, 'figure_5_climagrid_energy_sources_enhanced.png'))
plt.close()

# ------------------------------
# 5. Figure 6 – Spot Market Price and DER Dispatch
# ------------------------------
total_der_dispatch = battery_dispatch + fuel_cell_dispatch

fig, ax1 = plt.subplots(figsize=(12, 6), dpi=300)

color1 = 'tab:blue'
ax1.set_xlabel('Time', fontsize=16)
ax1.set_ylabel('Spot Market Price (EUR/MWh)', color=color1, fontsize=16)
ax1.plot(df_24h.index, price, color=color1, linewidth=2, label='Spot Market Price')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xticks(df_24h.index)
ax1.set_xticklabels(df_24h.index.strftime('%H:%M'), rotation=45, fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.6)

ax2 = ax1.twinx()
color2 = 'tab:green'
ax2.set_ylabel('DER Dispatch (kW)', color=color2, fontsize=16)
ax2.fill_between(df_24h.index, total_der_dispatch, step='mid', color=color2, alpha=0.4, label='Total DER Dispatch')
ax2.tick_params(axis='y', labelcolor=color2)

fig.tight_layout()
plt.title('Figure 6: Spot Market Price and ClimaGrid DER Dispatch Timeline', fontsize=18)
fig.savefig(os.path.join(save_path, 'figure_6_spot_price_der_dispatch.png'))
plt.close()

# ------------------------------
# 6. Summary Metrics
# ------------------------------
price_eur_kwh = price / 1000
cost_with_der = np.sum(grid_import * price_eur_kwh)
cost_without_der = np.sum(load * price_eur_kwh)

savings_pct = 100 * (1 - cost_with_der / cost_without_der)
peak_savings_pct = 100 * (1 - np.sum(grid_import[high_price] * price_eur_kwh[high_price]) /
                          np.sum(load[high_price] * price_eur_kwh[high_price]))

DER_peak_coverage = np.sum(battery_dispatch[high_price] + fuel_cell_dispatch[high_price]) / np.sum(load[high_price])
renewable_fraction = np.sum(renewable_used) / np.sum(load)

results = {
    "Total Energy Cost Reduction (%)": round(savings_pct, 1),
    "Cost Reduction During Price Peaks (%)": round(peak_savings_pct, 1),
    "DER Peak Coverage Ratio (%)": round(DER_peak_coverage * 100, 1),
    "Renewables Contribution to Total Demand (%)": round(renewable_fraction * 100, 1)
}

for k, v in results.items():
    print(f"{k}: {v}")
