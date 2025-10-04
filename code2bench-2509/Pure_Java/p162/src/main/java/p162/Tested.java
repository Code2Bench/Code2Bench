package p162;

public class Tested {
    /**
     * Calculates an offset based on the given parameters. The method evaluates the relationship between
     * the points (p1, p2) and (b1, b2) with respect to the dimensions (a1, a2). The offset is computed
     * based on the relative positions and dimensions, ensuring that the result is non-negative.
     *
     * <p>The method performs the following steps:
     * <ol>
     *   <li>If {@code b1} is less than or equal to {@code p1} or if {@code p1 + a1} is less than or equal to 0,
     *       the method returns 0 immediately.</li>
     *   <li>Otherwise, it calculates a determinant-like value {@code t = b1 * a2 - a1 * b2}.</li>
     *   <li>If {@code t} is positive, the method computes the offset based on the position of {@code p1}:
     *       <ul>
     *         <li>If {@code p1} is negative, the offset is calculated using {@code p1 * a2 / a1 - p2}.</li>
     *         <li>If {@code p1} is positive, the offset is calculated using {@code p1 * b2 / b1 - p2}.</li>
     *         <li>If {@code p1} is zero, the offset is simply {@code -p2}.</li>
     *       </ul>
     *   </li>
     *   <li>If {@code t} is not positive, the method computes the offset based on the relationship between
     *       {@code b1} and {@code p1 + a1}:
     *       <ul>
     *         <li>If {@code b1} is less than {@code p1 + a1}, the offset is {@code b2 - (p2 + (b1 - p1) * a2 / a1)}.</li>
     *         <li>If {@code b1} is greater than {@code p1 + a1}, the offset is {@code (a1 + p1) * b2 / b1 - (p2 + a2)}.</li>
     *         <li>If {@code b1} equals {@code p1 + a1}, the offset is {@code b2 - (p2 + a2)}.</li>
     *       </ul>
     *   </li>
     *   <li>Finally, if the computed offset is positive, it is returned; otherwise, 0 is returned.</li>
     * </ol>
     *
     * @param p1 The first coordinate of the point.
     * @param p2 The second coordinate of the point.
     * @param a1 The first dimension.
     * @param a2 The second dimension.
     * @param b1 The first coordinate of the reference point.
     * @param b2 The second coordinate of the reference point.
     * @return The calculated offset, which is always non-negative.
     */
    protected static double offset(double p1, double p2, double a1, double a2, double b1, double b2) {
        // Check if b1 is less than or equal to p1 or p1 + a1 is less than or equal to 0
        if (b1 <= p1 || (p1 + a1) <= 0) {
            return 0;
        }

        // Calculate determinant-like value t
        double t = b1 * a2 - a1 * b2;

        if (t > 0) {
            if (p1 < 0) {
                return (p1 * a2 / a1) - p2;
            } else if (p1 > 0) {
                return (p1 * b2 / b1) - p2;
            } else {
                return -p2;
            }
        } else {
            if (b1 < (p1 + a1)) {
                return b2 - (p2 + (b1 - p1) * a2 / a1);
            } else if (b1 > (p1 + a1)) {
                return ((a1 + p1) * b2 / b1) - (p2 + a2);
            } else {
                return b2 - (p2 + a2);
            }
        }

        // Return the offset if it's positive, else 0
        return Math.max(0, (double) Math.round((double) offset(p1, p2, a1, a2, b1, b2)));
    }
}