package p149;

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
        // TODO: implement this method
    }
}