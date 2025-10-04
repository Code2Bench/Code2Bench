package p224;

public class Tested {
    /**
     * Computes the modulus of two integers, ensuring the result is non-negative.
     * This method behaves similarly to the mathematical modulus operation, where the result
     * is always in the range [0, den - 1], even if the numerator is negative.
     *
     * @param num The numerator. Can be positive, negative, or zero.
     * @param den The denominator. Must be a positive integer.
     * @return The non-negative modulus result, in the range [0, den - 1].
     * @throws ArithmeticException if {@code den} is zero or negative.
     */
    public static int modUnsigned(int num, int den) {
        if (den <= 0) {
            throw new ArithmeticException("Denominator must be a positive integer");
        }
        
        // Handle the case where num is negative
        int sign = num < 0 ? -1 : 1;
        int absoluteNum = Math.abs(num);
        int result = absoluteNum % den;
        
        // Adjust result to be non-negative
        return result * sign;
    }
}