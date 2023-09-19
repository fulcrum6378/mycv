import numpy as np

arr: np.ndarray = np.array(
    [[1, 2, 3],
     [4, 5, 6]]
)
arr = np.reshape(arr, (3, 2))
print(arr)
