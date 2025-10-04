package p261;

import java.util.Arrays;

public class Tested {
    /**
     * Multiplies two matrices represented as one-dimensional arrays and returns the result as a new array.
     * The matrices are assumed to be stored in row-major order. The method performs matrix multiplication
     * where the number of columns in the first matrix (a) must match the number of rows in the second matrix (b).
     *
     * @param a The first matrix represented as a one-dimensional array in row-major order. Must not be null.
     * @param b The second matrix represented as a one-dimensional array in row-major order. Must not be null.
     * @param len The number of columns in the first matrix (a) and the number of rows in the second matrix (b).
     *            Must be greater than 0.
     * @return A new one-dimensional array representing the product of the two matrices in row-major order.
     * @throws IllegalArgumentException if either `a` or `b` is null, or if `len` is less than or equal to 0,
     *                                  or if the dimensions of the matrices are incompatible for multiplication.
     */
    public static float[] matrixMult(float[] a, float[] b, int len) {
        // Check for null values
        if (a == null || b == null) {
            throw new IllegalArgumentException("Matrices cannot be null");
        }
        
        // Check for len <= 0
        if (len <= 0) {
            throw new IllegalArgumentException("Length must be greater than 0");
        }
        
        // Check if the dimensions are compatible for multiplication
        int rowsA = len;
        int colsB = len;
        int rowsB = a.length / len;
        int colsA = b.length / len;
        
        if (rowsA != colsB || colsA != rowsB) {
            throw new IllegalArgumentException("Matrix dimensions are incompatible for multiplication");
        }
        
        // Calculate the result matrix
        float[] result = new float[rowsA * colsB];
        
        for (int i = 0; i < rowsA; i++) {
            for (int j = 0; j < colsB; j++) {
                float sum = 0;
                for (int k = 0; k < len; k++) {
                    sum += a[i * len + k] * b[k * len + j];
                }
                result[i * colsB + j] = sum;
            }
        }
        
        return result;
    }
}