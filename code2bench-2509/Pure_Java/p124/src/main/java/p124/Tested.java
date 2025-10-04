package p124;

public class Tested {
    /**
     * Converts a {@code long} value to an {@code int}, saturating the result if the value is outside
     * the range of an {@code int}. If the value is greater than {@link Integer#MAX_VALUE}, the method
     * returns {@link Integer#MAX_VALUE}. If the value is less than {@link Integer#MIN_VALUE}, the
     * method returns {@link Integer#MIN_VALUE}. Otherwise, the value is cast to an {@code int} and
     * returned.
     *
     * @param value the {@code long} value to be converted to an {@code int}
     * @return the saturated {@code int} value, which is either {@link Integer#MAX_VALUE},
     *         {@link Integer#MIN_VALUE}, or the cast value of {@code value}
     */
    public static int saturatedCast(long value) {
        int result = (int) value;
        if (result > Integer.MAX_VALUE) {
            return Integer.MAX_VALUE;
        }
        if (result < Integer.MIN_VALUE) {
            return Integer.MIN_VALUE;
        }
        return result;
    }
}