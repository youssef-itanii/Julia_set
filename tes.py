from dask.distributed import Client

import numpy as np
import dask.array as da

# client = Client(n_workers=4 , scheduler_port=44651)


a_da = da.ones(10, chunks=5)
a_da_sum = a_da.sum()
print(a_da_sum)
a_da_sum.visualize(engine="cytoscape")
a_da_sum.compute()
