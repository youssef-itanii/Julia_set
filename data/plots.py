import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dask_performance_path = 'dask_performance_2.csv'
ray_performance_path = 'ray_performance_2.csv'

dask_performance_data = pd.read_csv(dask_performance_path)
ray_performance_data = pd.read_csv(ray_performance_path)

dask_stats = dask_performance_data.groupby('Problem Size')['Execution Time'].describe()
ray_stats = ray_performance_data.groupby('Problem Size')['Execution Time'].describe()

plt.figure(figsize=(12, 6))

sns.lineplot(data=dask_performance_data, x='Problem Size', y='Execution Time', marker='o', label='Dask', color='red')

sns.lineplot(data=ray_performance_data, x='Problem Size', y='Execution Time', marker='o', label='Ray' ,)

plt.title('Execution Time Comparison between Dask and Ray')
plt.xlabel('Problem Size')
plt.ylabel('Execution Time (Seconds)')
plt.legend()
plt.grid(True)
plt.show()

dask_stats, ray_stats
