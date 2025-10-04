package p265;

import java.util.Arrays;

public class Tested {
    /**
     * Converts a segment of a byte array containing ASCII-encoded hexadecimal characters into a byte array.
     * Each pair of ASCII characters (representing a hexadecimal value) is converted into a single byte.
     * The method processes the input array from the specified start index (inclusive) to the end index (exclusive).
     *
     * <p>The method handles the following ASCII characters:
     * <ul>
     *   <li>Digits '0' to '9' are converted to their corresponding hexadecimal values (0x0 to 0x9).</li>
     *   <li>Lowercase letters 'a' to 'f' are converted to their corresponding hexadecimal values (0xA to 0xF).</li>
     *   <li>Uppercase letters 'A' to 'F' are converted to their corresponding hexadecimal values (0xA to 0xF).</li>
     * </ul>
     * Any other characters (e.g., linefeed) are skipped.
     *
     * <p>The method processes the input in pairs of characters, where the first character in the pair
     * contributes the high nibble (4 bits) of the resulting byte, and the second character contributes
     * the low nibble.
     *
     * @param data  the byte array containing ASCII-encoded hexadecimal characters. Must not be null.
     * @param start the starting index (inclusive) in the byte array to begin processing. Must be non-negative
     *              and less than the length of the array.
     * @param end   the ending index (exclusive) in the byte array to stop processing. Must be greater than or
     *              equal to the start index and less than or equal to the length of the array.
     * @return a byte array containing the converted hexadecimal values. The length of the returned array
     *         is half the number of valid hexadecimal character pairs processed.
     * @throws IllegalArgumentException if the start or end indices are invalid, or if the data array is null.
     */
    public static byte[] readASCII(byte[] data, int start, int end) {
        // TODO: implement this method
    }
}