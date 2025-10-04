package p218;

public class Tested {
    /**
     * Computes the modulus of two integers, ensuring the result is non-negative.
     * This method behaves similarly to the mathematical modulus operation, where the result
     * is always in the range [0, den - 1], even if the dividend (num) is negative.
     *
     * @param num The dividend. Can be any integer, including negative values.
     * @param den The divisor. Must be a positive integer; behavior is undefined if den is zero or negative.
     * @return The non-negative modulus result, in the range [0, den - 1].
     */
    public static int modUnsigned(int num, int den) {
        // Handle the case where den is zero or negative
        if (den <= 0) {
            throw new IllegalArgumentException("Denominator must be a positive integer.");
        }

        // Compute the modulus using Math.abs to ensure the result is non-negative
        return (int) Math.floorDiv(Math.abs(num), den) * den + Math.abs(num % den);
    }
}