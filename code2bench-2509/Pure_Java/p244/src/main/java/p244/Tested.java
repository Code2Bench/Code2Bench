package p244;

import java.util.NoSuchElementException;

public class Tested {
    /**
     * Searches for the end marker in the given byte array. The end marker is defined as two consecutive
     * bytes with the value 0x24 (ASCII '$'). The search starts from the 5th byte (index 4) and continues
     * until the second-to-last byte in the array.
     *
     * @param data The byte array to search for the end marker. Must not be null.
     * @return The index of the first byte of the end marker if found, or -1 if the end marker is not found.
     * @throws NullPointerException if the input array {@code data} is null.
     */
    public static int findEndMarker(byte[] data) {
        if (data == null) {
            throw new NullPointerException("data cannot be null");
        }

        // Check if the array has at least 5 bytes
        if (data.length < 5) {
            return -1;
        }

        // Start searching from index 4
        for (int i = 4; i < data.length - 1; i++) {
            if (data[i] == (byte) 0x24 && data[i + 1] == (byte) 0x24) {
                return i;
            }
        }

        return -1;
    }
}