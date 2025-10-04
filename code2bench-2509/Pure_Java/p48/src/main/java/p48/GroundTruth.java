package p48;
public class GroundTruth {
    public static String convertToHexadecimalString(byte[] hash) {
        StringBuilder sb = new StringBuilder(2 * hash.length);
        for (byte b : hash) {
            sb.append(String.format("%02x", b & 0xff));
        }

        return sb.toString();
    }
}