package p219;

import java.lang.Math;

public class Tested {
    /**
     * Computes the unsigned modulus of two floating-point numbers. This method ensures that the result
     * is always non-negative, even if the remainder of the division is negative. The result is equivalent
     * to the mathematical modulus operation, where the result lies in the range [0, den).
     *
     * <p>For example, {@code modUnsigned(5.5f, 3.0f)} returns 2.5f, and {@code modUnsigned(-1.5f, 4.0f)}
     * returns 2.5f.
     *
     * @param num The dividend, a floating-point number. Can be positive, negative, or zero.
     * @param den The divisor, a floating-point number. Must be non-zero.
     * @return The non-negative remainder of the division of {@code num} by {@code den}, in the range [0, den).
     * @throws ArithmeticException if {@code den} is zero.
     */
    public static float modUnsigned(float num, float den) {
        if (den == 0) {
            throw new ArithmeticException("divisor cannot be zero");
        }
        
        // Handle the case where the denominator is positive
        if (den > 0) {
            return (float) Math.abs(num % den);
        }
        
        // Handle the case where the denominator is negative
        else {
            return (float) Math.abs(num % den);
        }
    }
}