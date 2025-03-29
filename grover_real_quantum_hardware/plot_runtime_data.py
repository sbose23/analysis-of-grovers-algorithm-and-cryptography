import matplotlib.pyplot as plt
import json 

with open('./grover_real_quantum_hardware/Results/runtime_data.json', 'r') as f:
    runtime_data = json.load(f)

with open('./grover_real_quantum_hardware/Results/runtime_increase_trend.json', 'r') as f:
    runtime_increase_trend = json.load(f)

x1 = list(map(int, runtime_data.keys()))
y = list(runtime_data.values())

x2 = list(map(int, runtime_increase_trend.keys()))
z = list(runtime_increase_trend.values())

fig, ax1 = plt.subplots()

ax1.plot(x1, y, 'bo-', label='Runtime (s)')
ax1.set_xlabel('Bitstring length')
ax1.set_ylabel('Runtime (s)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

ax2 = ax1.twinx()
ax2.plot(x2, z, 'r^-', label='Runtime increase trend (%)')
ax2.set_ylabel('Runtime increase trend (%)', color='r')
ax2.tick_params(axis='y', labelcolor='r')

plt.title("Runtime & Runtime Increase Trend of Grover's Algorithm")
fig.tight_layout()
plt.grid(True)
plt.show()
