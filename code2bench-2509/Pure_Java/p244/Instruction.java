package p244;

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
        // TODO: implement this method
    }
}