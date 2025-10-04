package p184;

public class Tested {
    /**
     * Returns the smaller of two {@code double} values. If either value is NaN, the result is NaN.
     * This method considers the special case of -0.0 being smaller than +0.0.
     *
     * <p>The method performs the following checks in order:
     * <ol>
     *   <li>If {@code a} is greater than {@code b}, returns {@code b}.</li>
     *   <li>If {@code a} is less than {@code b}, returns {@code a}.</li>
     *   <li>If {@code a} and {@code b} are not equal (which includes the case where either is NaN), returns NaN.</li>
     *   <li>If {@code a} is -0.0, returns {@code a}.</li>
     *   <li>Otherwise, returns {@code b}.</li>
     * </ol>
     *
     * @param a the first {@code double} value
     * @param b the second {@code double} value
     * @return the smaller of {@code a} and {@code b}, or NaN if either value is NaN
     */
    public static double min(final double a, final double b) {
        // TODO: implement this method
    }
}