package p210;
public class GroundTruth {
    public static double entropy(byte[] bytes) {
        int n = 0;
        byte a = bytes[0];
        for (int i = 1; i < bytes.length; i++) {
            byte b = bytes[i];
            if (a != b) {
                n++;
                a = b;
            }
        }
        return n / (double) (bytes.length - 1);
    }
}