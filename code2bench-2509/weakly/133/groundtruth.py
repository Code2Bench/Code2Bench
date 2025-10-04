
import numpy

def k_mat(two_body_integrals):
    """
    Args:
        two_body_integrals: Numpy array of two-electron integrals with
            OpenFermion Ordering.

    Returns:
        k_matr : Numpy array of the exchange integrals K_{p,q} = (pq|qp)
            (in chemist notation).
    """
    chem_ordering = numpy.copy(two_body_integrals.transpose(0, 3, 1, 2), order='C')
    return numpy.einsum('ijji -> ij', chem_ordering)