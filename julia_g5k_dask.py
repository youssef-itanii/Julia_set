import csv
import os
from dask_jobqueue import OARCluster as Cluster
from dask.distributed import Client
from pprint import pprint
import logging
import time
import dask.array as da
from dask.distributed import progress
import numpy as np
import matplotlib.pyplot as plt
import sys




cluster = None
client = None

def julia_set(z, max_iterations, a):
    iterations_till_divergence = max_iterations + np.zeros(z.shape)
    for i in range(max_iterations):
        z = z**2 + a
        mask = (z * np.conj(z)) > 4
        iterations_till_divergence[mask] = i
        z[mask] = 0
    return iterations_till_divergence


def generate_julia(size, max_iterations,a,z_array_np ):
    print("Dask called")

    z_array = da.from_array(z_array_np, chunks=(size, size))
    result = da.map_blocks(julia_set, z_array, max_iterations, a, dtype=float)

    return result


def compute_performance(size, n_workers, cores_per_worker):

    start_time = time.time()
    max_iterations = 70
    a = -0.744 + 0.148j

    # Create a grid using NumPy's ogrid
    y, x = np.ogrid[1.4: -1.4: size*1j, -1.4: 1.4: size*1j]
    z_array_np = x + y*1j

    
    number_of_chunks = size//(n_workers)
    print(f"split data into {number_of_chunks} chunks ")
    result = generate_julia(number_of_chunks, max_iterations , a , z_array_np)
    # Compute the result and visualize
    plt.imshow(client.gather(result) ,cmap='twilight_shifted')
    plt.axis('off')

    # plt.savefig('my_image.png', bbox_inches='tight', pad_inches=0)

    end_time = time.time()
    execution_time = end_time - start_time
    file_name = 'performance_log_dask.csv'
    with open('performance_log_dask.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        # Check if file is empty and write headers if necessary
        if os.stat(file_name).st_size == 0:
            writer.writerow(['Problem Size', 'Execution Time', 'Number of Workers', 'Cores per Worker'])
        writer.writerow([size, execution_time, n_workers, cores_per_worker])


    
if __name__=="__main__":
    if(len(sys.argv) != 3):
        print(sys.argv)
        print("Usage: <number of workers> <number of cores per worker>")
        exit()
    
    n_workers = int(sys.argv[1])  # Number of workers
    cores_per_worker = int(sys.argv[2])  # Number of cores per worker
    cluster = Cluster(n_workers=n_workers, cores=cores_per_worker, memory="8GB")
    client = Client(cluster)
    print('OAR submission file: \n', cluster.job_script())

    for size in [1000 , 1500, 2000, 2500, 3000 , 6000, 12000, 15000]:  # Adjust this based on your needs
        compute_performance(size, n_workers, cores_per_worker)
    client.close()
    cluster.close()

