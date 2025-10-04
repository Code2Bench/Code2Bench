import numpy
import math

def orthogonalization_matrix(lengths, angles) -> numpy.ndarray:
    a, b, c = lengths
    alpha, beta, gamma = numpy.radians(angles)
    
    cos_alpha = math.cos(alpha)
    cos_beta = math.cos(beta)
    cos_gamma = math.cos(gamma)
    
    sin_alpha = math.sin(alpha)
    sin_beta = math.sin(beta)
    sin_gamma = math.sin(gamma)
    
    # Compute the orthogonalization matrix
    matrix = numpy.zeros((4, 4), dtype=float)
    matrix[0, 0] = a
    matrix[1, 1] = b
    matrix[2, 2] = c
    
    matrix[0, 1] = -b * cos_gamma
    matrix[0, 2] = -c * cos_beta
    
    matrix[1, 0] = -a * cos_gamma
    matrix[1, 2] = -c * cos_alpha
    
    matrix[2, 0] = a * sin_gamma
    matrix[2, 1] = b * sin_beta
    matrix[2, 2] = c * sin_alpha
    
    matrix[3, 3] = 1.0
    
    return matrix