from dask_jobqueue import OARCluster as Cluster
from dask.distributed import Client
from pprint import pprint
import logging
import os
import socket
import time
import dask.array as da
from dask.distributed import progress
import numpy as np
import matplotlib.pyplot as plt







def julia_set(z, max_iterations, a):
    print(f"Working on chunk of size {len(z)} ")
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


# def generate_julia(size, max_iterations,a,z_array_np ):
#     print("Dask called")
#     z_array = da.from_array(z_array_np, chunks=(size, size))
#     # future = client.scatter(z_array)
#     result = client.submit(julia_set, z_array , max_iterations ,a)
#     return result

if __name__=="__main__":
   
    workers = 6
    cluster = Cluster(
        queue='default',
        # Should be specified if you belongs to more than one GGA
        #project='<your grant access group>',
        cores=8,
        memory='16GiB',
        # The memory per core property name of your OAR cluster (usually memcore or mem_core).
        memory_per_core_property_name='memcore',
        # walltime for each worker job
        walltime='1:0:0',
        processes=workers,
    )

    cluster.scale(jobs=10)
    print('OAR submission file: \n', cluster.job_script())

    client = Client(cluster)

    size, max_iterations = 5000, 70
    a = -0.744 + 0.148j

    # Create a grid using NumPy's ogrid
    y, x = np.ogrid[1.4: -1.4: size*1j, -1.4: 1.4: size*1j]
    z_array_np = x + y*1j

    
    number_of_chunks = size//(workers*4)
    print(f"spint chunks into {number_of_chunks} ")
    start = time.time()
    result = generate_julia(number_of_chunks, max_iterations , a , z_array_np)
    # Compute the result and visualize
    plt.imshow(client.gather(result) ,cmap='twilight_shifted')
    plt.axis('off')

    plt.savefig('my_image.png', bbox_inches='tight', pad_inches=0)

    print(f"{time.time() - start} seconds")
    client.close()
    cluster.close()

