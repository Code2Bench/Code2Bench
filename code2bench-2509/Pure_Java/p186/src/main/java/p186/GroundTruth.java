package p186;
public class GroundTruth {
    public static float copySign(float magnitude, float sign) {
        int m = Float.floatToIntBits(magnitude);
        int s = Float.floatToIntBits(sign);
        if ((m >= 0 && s >= 0) || (m < 0 && s < 0)) { // Sign is currently OK
            return magnitude;
        }
        return -magnitude; // flip sign
    }
}