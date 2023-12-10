import time
import numpy as np
import matplotlib.pyplot as plt
from memory_profiler import memory_usage
import generate_julia_dask , generate_julia_seq , generate_julia_ray
from dask.distributed import Client

def measure_performance(func, *args, **kwargs):
    func_result = {}

    def wrapper():
        result = func(*args, **kwargs)
        func_result['result'] = result

    # Measure memory and record start/end time
    start_time = time.perf_counter()
    mem_usage = memory_usage(proc=(wrapper, ()), max_usage=True, retval=True)
    end_time = time.perf_counter()

    # Extracting the function result
    result = func_result.get('result', None)

    # Calculating execution time and peak memory usage
    exec_time = end_time - start_time

    return result, exec_time, mem_usage[0]

if __name__ =="__main__":
    
    # Test parameters
    size, max_iterations = 4000, 100
    y, x = np.ogrid[1.4: -1.4: size*1j, -1.4: 1.4: size*1j]
    a = -0.744 + 0.148j
    z_array_np = x + y*1j

    # seq_result, seq_time, seq_memory = None
    # seq_result, seq_time, seq_memory = measure_performance(generate_julia_seq.julia_set, size, size, max_iterations, a , z_array_np)


    # Measure performance for Ray
    num_of_workers_ray = int(generate_julia_ray.initialize_ray())
    ray_result, ray_time, ray_memory = measure_performance(generate_julia_ray.generate_julia,  num_of_workers_ray , max_iterations, a , z_array_np)
    print(f"Ray - Time: {ray_time} seconds, Memory: {ray_memory} MiB")

    # Measure performance for Dask
    client = Client(n_workers=num_of_workers_ray)
    num_workers_dask = len(client.scheduler_info()['workers'])
    print(F"{num_workers_dask} dask workers")
    
    dask_result, dask_time, dask_memory = measure_performance(generate_julia_dask.generate_julia, size/num_workers_dask, max_iterations, a , z_array_np )
    client.close()
    print(f"Dask - Time: {dask_time} seconds, Memory: {dask_memory} MiB")
    # Print results
    # print(f"Seq - Time: {seq_time} seconds, Memory: {seq_memory} MiB")
    # if(np.allclose(seq_result, ray_result, atol=1e-8) and np.allclose(dask_result, ray_result, atol=1e-8)):
    #     print(f"The final results are equal")
    # else:
    #     print(f"The final results are not equal")



    plt.imshow(ray_result, cmap='twilight_shifted')
    plt.title('Julia Set')
    plt.axis('off')


    plt.show()
