import csv
import os
from dask.distributed import Client
import time
import dask.array as da
import numpy as np
import matplotlib.pyplot as plt
import sys


client = None
def julia_set(z, max_iterations, a):
    iterations_till_divergence = max_iterations + np.zeros(z.shape)
    for i in range(max_iterations):
        z = z**2 + a
        mask = (z * np.conj(z)) > 4
        iterations_till_divergence[mask] = i
        z[mask] = 0
    return iterations_till_divergence

def generate_julia(size, max_iterations, a, z_array_np, chunk_size):
    z_array = da.from_array(z_array_np, chunks=(chunk_size, chunk_size))
    result = z_array.map_blocks(julia_set, max_iterations, a, dtype=float)

    return result

def compute_performance(size):
    total_threads = sum(worker['nthreads'] for worker in client.scheduler_info()['workers'].values())

    # chunk_size = size // int(np.sqrt(total_threads))
    if total_threads == 0:
        print("No threads found. Exiting...")
        exit()
    chunk_size = size // total_threads


    start_time = time.time()
    max_iterations = 70
    a = -0.744 + 0.148j

    y, x = np.ogrid[1.4: -1.4: chunk_size*1j, -1.4: 1.4: chunk_size*1j]
    z_array_np = x + y*1j

    result = generate_julia(chunk_size, max_iterations, a, z_array_np, chunk_size)

    # Compute and visualize
    plt.imshow(result.compute(), cmap='twilight_shifted')

    plt.axis('off')

    end_time = time.time()
    execution_time = end_time - start_time
    file_name = 'performance_log_dask.csv'
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        if os.stat(file_name).st_size == 0:
            writer.writerow(['Problem Size', 'Execution Time', 'Threads', 'Chunk Size'])
        writer.writerow([size, execution_time,total_threads ,chunk_size])
    plt.savefig('julia_set_plot_size_{}.png'.format(size), bbox_inches='tight', pad_inches=0)

def run_job(IP_address):
    global client
    try:
        client = Client("IP_address")
    except OSError:
        print("Unable to connect to server.")
        exit()
        

    start = 1000
    for _ in range(6):
        print(f"Working on size {start}")
        compute_performance(start)
        start*=2

    client.close()

if __name__ == "__main__":
    print(sys.argv)
    if(len(sys.argv) < 2):
        print("Missing IP Address")
    try:
        client = Client(sys.argv[1])
    except OSError:
        print("Unable to connect to server.")
        exit()
        

    start = 1000
    for _ in range(6):
        print(f"Working on size {start}")
        compute_performance(start)
        start*=2

    client.close()

