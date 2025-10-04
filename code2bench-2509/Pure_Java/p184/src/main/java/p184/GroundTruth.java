package p184;
public class GroundTruth {
    public static double min(final double a, final double b) {
        if (a > b) {
            return b;
        }
        if (a < b) {
            return a;
        }
        /* if either arg is NaN, return NaN */
        if (a != b) {
            return Double.NaN;
        }
        /* min(+0.0,-0.0) == -0.0 */
        /* 0x8000000000000000L == Double.doubleToRawLongBits(-0.0d) */
        long bits = Double.doubleToRawLongBits(a);
        if (bits == 0x8000000000000000L) {
            return a;
        }
        return b;
    }
}