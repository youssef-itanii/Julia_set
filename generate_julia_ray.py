import ray
import numpy as np
import matplotlib.pyplot as plt


def initialize_ray():
    ray.init()
    resources = ray.cluster_resources()
    num_workers = resources.get("CPU")
    print(F"{num_workers} Ray workers")
    return num_workers


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

    chunks = np.array_split(z_array_np, size)
    result_ids = [julia_set.remote(chunk, max_iterations, a) for chunk in chunks]
    results = ray.get(result_ids)
    final_result = np.concatenate(results)
    return final_result





if __name__=="__main__":
    h_range, w_range, max_iterations = 500, 500, 70
    a = -0.744 + 0.148j

    # Create a grid using NumPy's ogrid
    y, x = np.ogrid[1.4: -1.4: h_range*1j, -1.4: 1.4: w_range*1j]
    z_array_np = x + y*1j

    # Convert the array and split the array into chunks

    # Map the function to chunks of the new dask array
    final_result = generate_julia(max_iterations,a,z_array_np)

    # Compute the result and visualize
    plt.imshow(final_result, cmap='twilight_shifted', extent=[-1.4, 1.4, -1.4, 1.4])
    plt.colorbar(label='Iterations to Diverge')
    plt.title('Julia Set')
    plt.axis('off')
    plt.show()

    # Shutdown Ray
    ray.shutdown()
