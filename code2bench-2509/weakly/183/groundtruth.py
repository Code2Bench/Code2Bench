
import numpy as np

def _first_divided_difference(d, fct, fctder, atol=1e-12, rtol=1e-12):
    r"""First divided difference of a matrix function.

    First divided difference of a matrix function applied to the eigenvalues
    of a symmetric matrix. The first divided difference is defined as [1]_:

    .. math::
       [FDD(d)]_{i,j} =
           \begin{cases}
           \frac{fct(d_i)-fct(d_j)}{d_i-d_j},
           & d_i \neq d_j\\
           fctder(d_i),
           & d_i = d_j
           \end{cases}


    Parameters
    ----------
    d : ndarray, shape (n,)
        Eigenvalues of a symmetric matrix.
    fct : callable
        Function to apply to eigenvalues of d. Has to be defined for all
        possible eigenvalues of d.
    fctder : callable
        Derivative of the function to apply. Has to be defined for all
        possible eigenvalues of d.
    atol : float, default=1e-12
        Absolute tolerance for equality of eigenvalues.
    rtol : float, default=1e-12
        Relative tolerance for equality of eigenvalues.

    Returns
    -------
    FDD : ndarray, shape (n, n)
        First divided difference of the function applied to the eigenvalues.

    Notes
    -----
    .. versionadded:: 0.8

    References
    ----------
    .. [1] `Matrix  Analysis <https://doi.org/10.1007/978-1-4612-0653-8>`_
        R. Bhatia, Springer, 1997
    """
    dif = np.repeat(d[None, :], len(d), axis=0)

    close_ = np.isclose(dif, dif.T, atol=atol, rtol=rtol)
    dif[close_] = fctder(dif[close_])
    dif[~close_] = (fct(dif[~close_]) - fct(dif.T[~close_])) / \
                   (dif[~close_] - dif.T[~close_])
    return dif