from scipy import sparse
import numpy as np

def _build_dispersed_image_of_source(x: np.ndarray, y: np.ndarray, flux: np.ndarray) -> tuple[np.ndarray, list[int]]:
    # Find the minimum and maximum coordinates to determine image bounds
    minx, maxx = np.min(x), np.max(x)
    miny, maxy = np.min(y), np.max(y)
    
    # Create a sparse matrix using the coordinates and fluxes
    indices = np.vstack((x, y)).T
    sparse_matrix = sparse.coo_matrix((flux, (indices[:, 0], indices[:, 1])), shape=(maxx - minx + 1, maxy - miny + 1))
    
    # Convert the sparse matrix to a dense array
    image = sparse_matrix.toarray()
    
    # Return the image and the bounds
    return image, [minx, maxx, miny, maxy]