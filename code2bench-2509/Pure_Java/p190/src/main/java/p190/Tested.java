package p190;

import java.lang.Math;

public class Tested {
    /**
     * Computes the cube root of a given double value. The method handles three distinct cases:
     * <ul>
     *   <li>If the input value is greater than 0.000001, the cube root is calculated using the formula
     *       {@code Math.exp(Math.log(d) / 3.0)}.</li>
     *   <li>If the input value is between -0.000001 and 0.000001 (inclusive), the method returns 0.</li>
     *   <li>If the input value is less than -0.000001, the cube root is calculated as the negative of
     *       the cube root of the absolute value of the input, using the formula
     *       {@code -Math.exp(Math.log(-d) / 3.0)}.</li>
     * </ul>
     *
     * @param d the double value for which to compute the cube root
     * @return the cube root of the input value, as a double
     */
    private static double sqrt3(double d) {
        if (d > 0.000001) {
            return Math.exp(Math.log(d) / 3.0);
        } else if (d >= -0.000001 && d <= 0.000001) {
            return 0.0;
        } else {
            return -Math.exp(Math.log(-d) / 3.0);
        }
    }
}