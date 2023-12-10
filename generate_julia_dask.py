import dask.array as da
from dask.distributed import progress
import numpy as np
import matplotlib.pyplot as plt

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
    progress(result)
    result.visualize()
    return result.compute()



# if __name__=="__main__":

#     h_range, w_range, max_iterations = 500, 500, 70
#     a = -0.744 + 0.148j

#     # Create a grid using NumPy's ogrid
#     y, x = np.ogrid[1.4: -1.4: h_range*1j, -1.4: 1.4: w_range*1j]
#     z_array_np = x + y*1j

#     # Convert the array and split the array into chunks
#     print("here")
#     z_array = da.from_array(z_array_np, chunks=(h_range // 100, w_range // 100))

#     # Map the function to chunks of the new dask array
#     result = da.map_blocks(julia_set, z_array, max_iterations, a, dtype=float)
#     # Compute the result and visualize
#     plt.imshow(result.compute(), cmap='twilight_shifted')
#     result.visualize()
#     plt.axis('off')
#     plt.show()
