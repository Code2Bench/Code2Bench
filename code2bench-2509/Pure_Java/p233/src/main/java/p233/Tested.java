public class Tested {
    /**
     * Adjusts the length of the provided byte array to match the specified target length.
     * If the original key's length is equal to the target length, the original key is returned unchanged.
     * If the original key is shorter than the target length, it is padded with zeros to reach the target length.
     * If the original key is longer than the target length, it is truncated to the target length.
     *
     * @param originalKey The original byte array to be adjusted. Must not be null.
     * @param targetLength The desired length of the resulting byte array. Must be non-negative.
     * @return A new byte array with the adjusted length, either padded or truncated as necessary.
     * @throws IllegalArgumentException if {@code originalKey} is null or {@code targetLength} is negative.
     */
    public static byte[] adjustKeyLength(byte[] originalKey, int targetLength) {
        if (originalKey == null || targetLength < 0) {
            throw new IllegalArgumentException("originalKey cannot be null and targetLength cannot be negative");
        }

        int originalLength = originalKey.length;
        if (originalLength == targetLength) {
            return Arrays.copyOf(originalKey, targetLength);
        } else if (originalLength < targetLength) {
            // Pad with zeros
            byte[] padded = new byte[targetLength];
            System.arraycopy(originalKey, 0, padded, 0, originalLength);
            return padded;
        } else {
            // Truncate to target length
            return Arrays.copyOf(originalKey, targetLength);
        }
    }
}