
import numpy

def j_mat(two_body_integrals):
    """
    Args:
        two_body_integrals: Numpy array of two-electron integrals with
            OpenFermion Ordering.

    Returns:
        j_matr : Numpy array of the coulomb integrals J_{p,q} = (pp|qq)
            (in chemist notation).
    """
    chem_ordering = numpy.copy(two_body_integrals.transpose(0, 3, 1, 2), order='C')
    return numpy.einsum('iijj -> ij', chem_ordering)