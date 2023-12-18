import matplotlib.pyplot as plt
import seaborn as sns


import pandas as pd

# Load the data for analysis
dask_file_path = 'dask_performance.csv'
ray_file_path = 'ray_performance.csv'

dask_data = pd.read_csv(dask_file_path)
ray_data = pd.read_csv(ray_file_path)

# Displaying the first few rows of each dataframe to understand their structure
dask_data.head(), ray_data.head()

# Setting up the visualization
sns.set(style="whitegrid")

# Plotting Dask Performance
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
sns.lineplot(data=dask_data, x='Problem Size', y='Execution Time', hue='Threads', marker='o')
plt.title('Dask Performance')
plt.xlabel('Problem Size')
plt.ylabel('Execution Time (s)')

# Plotting Ray Performance
plt.subplot(1, 2, 2)
sns.lineplot(data=ray_data, x='Problem Size', y='Execution Time', hue='Number of Workers', marker='o')
plt.title('Ray Performance')
plt.xlabel('Problem Size')
plt.ylabel('Execution Time (s)')

plt.tight_layout()
plt.show()
