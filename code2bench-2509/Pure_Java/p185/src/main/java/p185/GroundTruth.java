package p185;
public class GroundTruth {
    public static double copySign(double magnitude, double sign) {
        long m = Double.doubleToLongBits(magnitude);
        long s = Double.doubleToLongBits(sign);
        if ((m >= 0 && s >= 0) || (m < 0 && s < 0)) { // Sign is currently OK
            return magnitude;
        }
        return -magnitude; // flip sign
    }
}