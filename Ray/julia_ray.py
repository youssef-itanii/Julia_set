import csv
import sys
import ray
import numpy as np
import matplotlib.pyplot as plt
import time
import os



@ray.remote
def julia_set(z, max_iterations, a):
    iterations_till_divergence = max_iterations + np.zeros(z.shape)
    for i in range(max_iterations):
        z = z**2 + a
        mask = (z * np.conj(z)) > 4
        iterations_till_divergence[mask] = i
        z[mask] = 0
    return iterations_till_divergence

def generate_julia(size ,max_iterations,a,z_array_np):

    chunk_size = size // num_workers
    remainder = size % num_workers

    chunks = []
    start = 0
    for i in range(num_workers):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunk = z_array_np[start:end]
        chunks.append(chunk)
        start = end

    result_ids = [julia_set.remote(chunk, max_iterations, a) for chunk in chunks]
    results = ray.get(result_ids)

    final_result = np.concatenate(results)
    return final_result




def main(size, num_workers, num_cpus):

    max_iterations = 70
    a = -0.744 + 0.148j

    y, x = np.ogrid[1.4: -1.4: size*1j, -1.4: 1.4: size*1j]
    z_array_np = x + y*1j

    start_time = time.time()

    final_result = generate_julia(size , max_iterations,a,z_array_np)

    end_time = time.time()
    execution_time = end_time - start_time
    file_name = "performance_log_ray.csv"
    print(f"{size}, {execution_time}, {num_workers}, {num_cpus}")
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        if os.stat(file_name).st_size == 0:
            writer.writerow(['Problem Size', 'Execution Time', 'Threads', 'Total CPUs'])
        writer.writerow([size, execution_time, num_workers, num_cpus])

if __name__ == "__main__":

    ray.init(
        address='auto', 
    )

    resources = ray.cluster_resources()
    num_workers = int(resources.get("CPU"))
    num_cpus = resources.get("CPU")
    print('Problem Size, Execution Time, Number of Workers,Total CPUs')
    start = 1000
    for i in range(6):  # Adjust this based on your needs
        main(start, num_workers, num_cpus)
        start*=2

    ray.shutdown()  # Shut down Ray at the end


