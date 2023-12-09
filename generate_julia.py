import time
import numpy as np
import matplotlib.pyplot as plt
import generate_julia_dask , generate_julia_seq


def generate_seq(h_range,w_range,max_iterations,a,z_array_np):
    generate_plot(generate_julia_seq.julia_set(h_range,w_range,max_iterations,a,z_array_np))

def generate_dask(z, max_iterations, a):
    generate_plot(generate_julia_dask.julia_set(z , max_iterations , a))

def generate_plot(julia_set):
    plt.imshow(julia_set, cmap='twilight_shifted')
    plt.axis('off')
    plt.show()
    plt.close()

if __name__=="__main__":

    h_range, w_range, max_iterations = 500, 500, 70
    y, x = np.ogrid[1.4: -1.4: h_range*1j, -1.4: 1.4: w_range*1j]
    a = -0.744 + 0.148j
    z_array_np = x + y*1j
    start = time.time()
    generate_seq(h_range,w_range,max_iterations,a,z_array_np)
    end = time.time() - start

    print(f"Sequential Code took {end} seconds")