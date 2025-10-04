package p258;
public class GroundTruth {
    public static byte[] asBytes(String basicString) {
        final byte[] b = new byte[basicString.length()];
        for (int i = 0; i < b.length; ++i) {
            b[i] = (byte) basicString.charAt(i);
        }
        return b;
    }
}