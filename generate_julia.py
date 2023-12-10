import time
import numpy as np
import matplotlib.pyplot as plt
import generate_julia_dask , generate_julia_seq , generate_julia_ray


def generate_seq(h_range,w_range,max_iterations,a,z_array_np):
    start = time.time()

    generate_plot(generate_julia_seq.julia_set(h_range,w_range,max_iterations,a,z_array_np))
    end = time.time() - start

    print(f"Sequential Code took {end} seconds")

def generate_dask(h_range,w_range,max_iterations,a,z_array_np):
    start = time.time()
    generate_plot(generate_julia_dask.generate_julia(h_range,w_range,max_iterations,a,z_array_np , max_iterations/100))
    end = time.time() - start

    print(f"DASK Code took {end} seconds")

def generate_ray(max_iterations,a,z_array_np):
    start = time.time()
    generate_plot(generate_julia_ray.generate_julia(max_iterations,a,z_array_np , 10))
    end = time.time() - start

    print(f"Ray Code took {end} seconds")


def generate_plot(julia_set):
    plt.imshow(julia_set, cmap='twilight_shifted')
    plt.axis('off')
    plt.show()
    plt.close()

if __name__=="__main__":

    h_range, w_range, max_iterations = 1000, 1000, 1000
    y, x = np.ogrid[1.4: -1.4: h_range*1j, -1.4: 1.4: w_range*1j]
    a = -0.744 + 0.148j
    z_array_np = x + y*1j
    # generate_seq(h_range,w_range,max_iterations,a,z_array_np)
    generate_dask(h_range,w_range,max_iterations,a,z_array_np)
    generate_ray(max_iterations,a,z_array_np)