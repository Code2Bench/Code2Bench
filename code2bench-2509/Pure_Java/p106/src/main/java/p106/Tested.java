package p106;

import java.math.BigDecimal;

public class Tested {
    /**
     * Performs integer division of {@code x} by {@code y} and rounds the result towards positive infinity.
     * This method behaves similarly to the mathematical ceiling function for division.
     *
     * <p>If both {@code x} and {@code y} have the same sign (both positive or both negative) and the division
     * does not result in an exact quotient (i.e., there is a remainder), the result is incremented by 1.
     * Otherwise, the result is the exact quotient.
     *
     * @param x the dividend
     * @param y the divisor (must not be zero)
     * @return the smallest integer greater than or equal to the exact quotient of {@code x} divided by {@code y}
     * @throws ArithmeticException if {@code y} is zero
     */
    public static int ceilDiv(int x, int y) {
        if (y == 0) {
            throw new ArithmeticException("Division by zero");
        }

        // Handle the case where y is positive
        if (y > 0) {
            return (int) Math.ceil((double) x / y);
        } else {
            // Handle the case where y is negative
            return (int) Math.ceil((double) x / y);
        }
    }
}