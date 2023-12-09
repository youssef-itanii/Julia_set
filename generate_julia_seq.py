#! python3
import numpy as np 
import matplotlib.pyplot as plt 

def julia_set(h_range, w_range, max_iterations , a , z_array):
    ''' 
    SOURCE: https://blbadger.github.io/julia-sets.html
    
    A function to determine the values of the Julia set. Takes
    an array size specified by h_range and w_range, in pixels, along
    with the number of maximum iterations to try.  Returns an array with 
    the number of the last bounded iteration at each array value.
    '''
    
    iterations_till_divergence = max_iterations + np.zeros(z_array.shape)
    for h in range(h_range):
        for w in range(w_range):
            z = z_array[h][w]
            for i in range(max_iterations):
                z = z**2 + a
                if z * np.conj(z) > 4:
                    iterations_till_divergence[h][w] = i
                    break

    return iterations_till_divergence

