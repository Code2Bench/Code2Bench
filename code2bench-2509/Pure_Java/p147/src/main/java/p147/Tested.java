package p147;

import java.util.Arrays;

public class Tested {
    /**
     * Converts a byte array into a hexadecimal string representation. Each byte is converted to two
     * hexadecimal characters, separated by a space. The hexadecimal characters are uppercase.
     *
     * <p>For example, the byte array {@code [0x1A, 0x2B]} will be converted to the string
     * {@code "1A 2B "}.
     *
     * @param bytes the byte array to be converted. If {@code null}, the behavior is undefined.
     * @return a string representing the hexadecimal values of the bytes, separated by spaces.
     *         The returned string will have a length of {@code bytes.length * 3} (including spaces).
     *         If the input array is empty, an empty string is returned.
     */
    public static String hexify(byte[] bytes) {
        if (bytes == null || bytes.length == 0) {
            return "";
        }

        StringBuilder result = new StringBuilder();
        for (byte b : bytes) {
            result.append(String.format("%02X", b));
            result.append(" ");
        }
        return result.toString().trim();
    }
}