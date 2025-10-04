package p41;
public class GroundTruth {
    public static String bytesToHex(byte[] hash) {
        char[] hexArray = "0123456789abcdef".toCharArray();
        char[] hexChars = new char[hash.length * 2];
        for (int i = 0; i < hash.length; i++) {
            int v = hash[i] & 0xFF;
            hexChars[i * 2] = hexArray[v >>> 4];
            hexChars[i * 2 + 1] = hexArray[v & 0x0F];
        }
        return new String(hexChars);
    }
}