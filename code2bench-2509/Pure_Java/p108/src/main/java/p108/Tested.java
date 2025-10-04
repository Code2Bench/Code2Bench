package p108;

public class Tested {
    /**
     * Computes the floor division of two long values. The result is the largest (closest to positive infinity)
     * long value that is less than or equal to the algebraic quotient of the two values. This method handles
     * negative remainders correctly by adjusting the result to ensure it is the floor value.
     *
     * @param a the dividend
     * @param b the divisor (must not be zero)
     * @return the floor value of the division of {@code a} by {@code b}
     * @throws ArithmeticException if {@code b} is zero
     */
    public static long floor(long a, long b) {
        if (b == 0) {
            throw new ArithmeticException("Division by zero");
        }
        
        // Handle positive and negative numbers
        long result = (a / b);
        
        // If the remainder is negative, adjust the result to be the floor value
        if (a % b < 0) {
            result -= 1;
        }
        
        return result;
    }
}