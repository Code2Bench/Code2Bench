package p264;

import java.util.Objects;

public class Tested {
    /**
     * Decrypts a portion of a byte array using a custom decryption algorithm.
     *
     * <p>The decryption process involves iterating over the specified range of the input byte array,
     * applying a transformation using the provided key, and skipping a specified number of bytes
     * at the beginning of the range. The transformation is based on a combination of XOR operations
     * and modular arithmetic using constants 52845 and 22719.</p>
     *
     * <p>If the effective length of the decrypted data (after accounting for the skip) is negative,
     * the skip value is reset to 0 to ensure valid array creation.</p>
     *
     * @param d    the input byte array to decrypt; must not be null
     * @param start the starting index (inclusive) of the range to decrypt
     * @param end   the ending index (exclusive) of the range to decrypt
     * @param key   the decryption key used in the transformation
     * @param skip  the number of bytes to skip at the beginning of the range
     * @return a new byte array containing the decrypted data
     * @throws NullPointerException if the input byte array {@code d} is null
     */
    private static byte[] decrypt(byte[] d, int start, int end, int key, int skip) {
        if (d == null) {
            throw new NullPointerException("Input byte array cannot be null");
        }

        // Calculate effective length after skip
        int effectiveLength = end - start;
        if (effectiveLength < 0) {
            effectiveLength = 0;
            skip = 0;
        }

        // Ensure skip does not exceed the effective length
        skip = Math.max(0, Math.min(skip, effectiveLength));

        // Create a new byte array for the result
        byte[] result = new byte[effectiveLength];

        // Iterate over the specified range
        for (int i = 0; i < effectiveLength; i++) {
            int index = start + skip + i;
            if (index >= d.length) {
                break;
            }

            // Apply the decryption transformation
            int value = d[index];
            int transformedValue = (value ^ key) % 52845;
            transformedValue = (transformedValue + 22719) % 52845;

            result[i] = (byte) transformedValue;
        }

        return result;
    }
}