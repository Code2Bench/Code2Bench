package p233;
public class GroundTruth {
    public static byte[] adjustKeyLength(byte[] originalKey, int targetLength) {
        if (originalKey.length == targetLength) {
            return originalKey;
        }
        else if (originalKey.length < targetLength) {
            byte[] paddedKey = new byte[targetLength];
            System.arraycopy(originalKey, 0, paddedKey, 0, originalKey.length);
            return paddedKey;
        }
        else {
            byte[] truncatedKey = new byte[targetLength];
            System.arraycopy(originalKey, 0, truncatedKey, 0, targetLength);
            return truncatedKey;
        }
    }
}