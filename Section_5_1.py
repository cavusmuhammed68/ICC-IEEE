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

df_last24 = df.tail(24).copy()
time = df_last24['time']
load = df_last24['consumption'].values
pv = df_last24['pv_production'].values

# ------------------------------
# 2. System Parameters
# ------------------------------
battery_capacity = 5.0  # kWh
battery_power_limit = 2.0  # kW
battery_soc = 0.5 * battery_capacity
efficiency = 0.95

fuel_cell_power_limit = 2.0  # kW
fuel_cell_energy = 10.0  # kWh

flexible_load_ratio = 0.3

# Initialise arrays
apad_load = load.copy()
battery_dispatch = np.zeros_like(load)
fuel_cell_dispatch = np.zeros_like(load)

# ------------------------------
# 3. Adaptive Priority-Aware Dispatch (APAD) Logic
# ------------------------------
for t in range(len(load)):
    net_load = load[t] - pv[t]

    if net_load < 0:
        # Excess PV → charge battery
        available_pv = -net_load
        charge = min(available_pv, battery_power_limit, (battery_capacity - battery_soc) / efficiency)
        battery_soc += charge * efficiency
        battery_dispatch[t] = -charge
    else:
        remaining = net_load

        # Battery discharge
        discharge = min(remaining, battery_power_limit, battery_soc)
        battery_soc -= discharge
        battery_dispatch[t] = discharge
        remaining -= discharge

        # Fuel cell supply
        if remaining > 0 and fuel_cell_energy > 0:
            fc_out = min(remaining, fuel_cell_power_limit, fuel_cell_energy)
            fuel_cell_dispatch[t] = fc_out
            fuel_cell_energy -= fc_out
            remaining -= fc_out

        # Optimised load using APAD
        apad_load[t] = load[t] - battery_dispatch[t] - fuel_cell_dispatch[t]

# ------------------------------
# 4. Optional Load Shifting
# ------------------------------
for t in range(1, len(apad_load)-1):
    if apad_load[t] > np.mean(apad_load):
        shift_amount = min(flexible_load_ratio * load[t], apad_load[t] - np.mean(apad_load))
        apad_load[t] -= shift_amount
        apad_load[t+1] += shift_amount / 2
        apad_load[t-1] += shift_amount / 2

# ------------------------------
# 5. Statistics
# ------------------------------
print("\n--- APAD LOAD OPTIMISATION STATS (Last 24 Hours) ---")
print(f"Peak Load Before: {np.max(load):.2f} kW")
print(f"Peak Load After (APAD):  {np.max(apad_load):.2f} kW")
print(f"Peak-to-Average Before: {np.max(load)/np.mean(load):.2f}")
print(f"Peak-to-Average After (APAD):  {np.max(apad_load)/np.mean(apad_load):.2f}")
print(f"Fuel Cell Energy Used: {np.sum(fuel_cell_dispatch):.2f} kWh")

# ------------------------------
# 6. Plot: Load Profile (APAD)
# ------------------------------
plt.figure(figsize=(12, 6), dpi=600)
plt.plot(time, load, label='Original Load', linewidth=2)
plt.plot(time, apad_load, label='Optimised Load (APAD)', linestyle='--', linewidth=2, color='orange')
plt.xlabel('Time', fontsize=16)
plt.ylabel('Load (kW)', fontsize=16)
plt.title('Load Profile Optimisation – APAD Method (Last 24 Hours)', fontsize=18)
plt.legend(fontsize=14)
plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(save_path, 'figure_5_1_load_profile.png'))
plt.close()

# ------------------------------
# 6. Step Plot: Load Profile (APAD)
# ------------------------------
plt.figure(figsize=(12, 6), dpi=600)
plt.step(time, load, where='mid', label='Original Load', linewidth=2)
plt.step(time, apad_load, where='mid', label='Optimised Load (APAD)', linestyle='--', linewidth=2, color='orange')
plt.xlabel('Time', fontsize=16)
plt.ylabel('Load (kW)', fontsize=16)
plt.title('Load Profile Optimisation – APAD Method (Last 24 Hours)', fontsize=18)
plt.legend(fontsize=14)
plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(save_path, 'figure_5_1_load_profile.png'))
plt.close()

