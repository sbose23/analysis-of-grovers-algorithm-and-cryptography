import matplotlib.pyplot as plt
import json
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

with open('./grover_runtime_analysis/Results/runtime_data_2-17_Bits.json', 'r') as f:
    runtime_data = json.load(f)

with open('./grover_runtime_analysis/Results/runtime_increase_data_2-17_Bits.json', 'r') as f:
    runtime_increase_trend = json.load(f)

# Convert string keys to integers
keys_time = list(map(int, runtime_data.keys()))
values_time = list(runtime_data.values())

keys_inc = list(map(int, runtime_increase_trend.keys()))
values_inc = list(runtime_increase_trend.values())

fig, axes = plt.subplots(1, 2, figsize=(18, 9), gridspec_kw={'wspace': 0.2})  # Increased figure size

# Plot raw runtime data
axes[0].plot(keys_time, values_time, marker='o', linestyle='-', color='b', label='Runtime')
axes[0].set_xlabel('Bitstring length')
axes[0].set_ylabel('Runtime (s)')
axes[0].set_title('Runtime Trend of Grover\'s Algorithm On Simulator')
axes[0].legend()

# Inset zoom for raw runtime
axins1 = inset_axes(axes[0], width='40%', height='40%', loc='upper left', borderpad=5)
axins1.plot(keys_time[:9], values_time[:9], marker='o', linestyle='-', color='b')
axins1.set_xticks(keys_time[:9])
axins1.set_title('Zoomed In (2-10)')

# Plot percentage increase data
axes[1].plot(keys_inc, values_inc, marker='s', linestyle='-', color='r', label='Percentage Increase')
axes[1].set_xlabel('Bitstring length')
axes[1].set_ylabel('Percentage increase (%)')
axes[1].set_title('Runtime Increase Trend of Grover\'s Algorithm On Simulator')
axes[1].legend()

plt.tight_layout()
plt.show()
