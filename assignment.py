import numpy as np

np.random.seed(42)

num_customers = 500
inter_arrival_times = np.random.uniform(1, 8, size=num_customers).astype(int)
service_times = np.random.uniform(1, 6, size=num_customers).astype(int)

# print(service_times)
arrival_times = np.cumsum(inter_arrival_times)
start_times = []
end_times = []
wait_times = []
time_in_system = []

server_available_time = 0

for i in range(num_customers):
    start_time = max(arrival_times[i], server_available_time)
    end_time = start_time + service_times[i]
    total_time = end_time - arrival_times[i]

    wait_time = start_time - arrival_times[i]
    
    start_times.append(start_time)
    end_times.append(end_time)
    wait_times.append(wait_time)
    time_in_system.append(total_time)

    
    server_available_time = end_time

average_wait = np.mean(wait_times)
average_service = np.mean(service_times)
average_system_time = np.mean(np.array(end_times) - arrival_times)
utilization = sum(service_times) / end_times[-1]
print(utilization)

import pandas as pd

df = pd.DataFrame({
    "Customer ID": np.arange(1, num_customers + 1),
    "Arrival Time": np.round(arrival_times, 2),
    "Service Start Time": np.round(start_times, 2),
    "Service End Time": np.round(end_times, 2),
    "Service Time": np.round(service_times, 2),
    "Waiting Time": np.round(wait_times, 2),
    "Time in System": np.round(time_in_system, 2)
})
print(df.head())

# performance to 2 dp
print(f"Average wait time: {df['Waiting Time'].mean():.2f} mins")
print(f"Average service time: {df['Service Time'].mean():.2f} mins")
print(f"Average time in system: {df['Time in System'].mean():.2f} mins")
print(f"Server utilization: {utilization:.2%}")

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(20, 12))
ax.axis('off')
table = ax.table(cellText=df.head(15).values,
                 colLabels=df.columns,
                 loc='center',
                 cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)  # Increase font
table.scale(1.5, 1.5)   # Bigger cells

colors = ['#f2f2f2', 'white']
for i in range(len(df.head(15))):
    for j in range(len(df.columns)):
        table[(i+1, j)].set_facecolor(colors[i % 2])

for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold', color='black')
        cell.set_facecolor('#d0d0d0')
    cell.set_linewidth(0.6)
    cell.set_edgecolor('gray')

plt.title("Bank Queue Simulation - First 15 Customers", fontsize=14)
plt.savefig("simulation_table_preview.png", bbox_inches='tight')
plt.show()