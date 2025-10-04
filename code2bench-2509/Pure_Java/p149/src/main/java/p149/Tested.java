package p149;

import java.util.Arrays;

public class Tested {
    /**
     * Converts a 4-byte array representing hexadecimal characters into its corresponding integer value.
     * The method processes each byte in the array, interpreting it as a hexadecimal digit (0-9, a-f, or A-F).
     * If any byte is not a valid hexadecimal character, the method returns -1.
     *
     * The method assumes that the input array contains exactly 4 bytes. If the array is shorter, the behavior
     * is undefined and may result in an {@code ArrayIndexOutOfBoundsException}.
     *
     * @param hex A byte array of length 4, where each byte represents a hexadecimal character.
     * @return The integer value corresponding to the hexadecimal representation, or -1 if any byte is invalid.
     */
    public static int unhex(byte[] hex) {
        // Check if the input array has exactly 4 bytes
        if (hex.length != 4) {
            return -1;
        }

        // Check each byte in the array
        for (byte b : hex) {
            if (!isHexDigit(b)) {
                return -1;
            }
        }

        // Convert the hexadecimal string to integer
        int result = 0;
        for (byte b : hex) {
            result = (result << 4) | (b & 0xF);
        }

        return result;
    }

    private static boolean isHexDigit(byte b) {
        return (b >= 0x30 && b <= 0x39) || (b >= 0x41 && b <= 0x46) || (b >= 0x61 && b <= 0x66);
    }
}