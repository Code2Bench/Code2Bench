package p185;

import java.lang.Double;

public class Tested {
    /**
     * Returns the first floating-point argument with the sign of the second floating-point argument.
     * The magnitude of the result is the same as the first argument, but the sign is set to match
     * the sign of the second argument. If the signs of both arguments are already the same, the
     * first argument is returned unchanged. Otherwise, the sign of the first argument is flipped.
     *
     * <p>This method handles all possible double values, including positive and negative zero,
     * infinity, and NaN. The sign of NaN is preserved according to the second argument.
     *
     * @param magnitude the value whose magnitude is used in the result
     * @param sign the value whose sign is used in the result
     * @return a value with the magnitude of {@code magnitude} and the sign of {@code sign}
     */
    public static double copySign(double magnitude, double sign) {
        if (Double.compare(sign, 0.0) == 0) {
            return magnitude > 0.0 ? magnitude : -magnitude;
        }
        
        if (Double.compare(magnitude, 0.0) == 0) {
            return sign > 0.0 ? sign : -sign;
        }
        
        if (Double.compare(sign, 0.0) == 0 && Double.compare(magnitude, 0.0) == 0) {
            return 0.0;
        }
        
        return (double) Math.copySign(magnitude, sign);
    }
}