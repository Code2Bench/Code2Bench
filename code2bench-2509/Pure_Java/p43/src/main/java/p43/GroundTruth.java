package p43;
public class GroundTruth {
    public static String encodeHex(byte[] digest) {
        StringBuilder sb = new StringBuilder();
        for (byte b : digest) {
            sb.append(Integer.toString((b & 0xFF) + 256, 16).substring(1));
        }
        return sb.toString();
    }
}