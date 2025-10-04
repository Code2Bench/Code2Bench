package p186;

import java.util.*;

public class Tested {
    /**
     * Returns a float with the magnitude of the first argument and the sign of the second argument.
     * If the sign of the second argument is already the same as the sign of the first argument,
     * the first argument is returned unchanged. Otherwise, the sign of the first argument is flipped.
     *
     * @param magnitude The float value whose magnitude is to be used. Can be positive, negative, or zero.
     * @param sign The float value whose sign is to be used. Can be positive, negative, or zero.
     * @return A float with the magnitude of {@code magnitude} and the sign of {@code sign}.
     */
    public static float copySign(float magnitude, float sign) {
        if (sign > 0 && magnitude > 0) {
            return magnitude;
        } else if (sign < 0 && magnitude < 0) {
            return magnitude;
        } else {
            return -magnitude;
        }
    }
}