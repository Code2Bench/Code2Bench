package p261;

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
        // TODO: implement this method
    }
}