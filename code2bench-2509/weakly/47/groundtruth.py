
from scipy import sparse

def _build_dispersed_image_of_source(x, y, flux):
    """
    Convert a flattened list of pixels to a 2-D grism image of that source.

    Parameters
    ----------
    x : ndarray
        X coordinates of pixels in the grism image
    y : ndarray
        Y coordinates of pixels in the grism image
    flux : ndarray
        Fluxes of pixels in the grism image

    Returns
    -------
    _type_
        _description_
    """
    minx = int(min(x))
    maxx = int(max(x))
    miny = int(min(y))
    maxy = int(max(y))
    a = sparse.coo_matrix(
        (flux, (y - miny, x - minx)), shape=(maxy - miny + 1, maxx - minx + 1)
    ).toarray()
    bounds = [minx, maxx, miny, maxy]
    return a, bounds