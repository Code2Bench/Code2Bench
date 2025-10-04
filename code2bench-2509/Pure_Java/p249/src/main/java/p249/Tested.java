package p249;

import java.util.Objects;

public class Tested {
    /**
     * Converts a byte array to a hexadecimal string representation. Each byte is formatted as a two-digit
     * uppercase hexadecimal value, separated by a single space. The resulting string is trimmed of any trailing
     * whitespace.
     *
     * <p>For example, the byte array {@code {0x1A, 0x2B, 0x3C}} will be converted to the string
     * {@code "1A 2B 3C"}.
     *
     * @param bytes the byte array to convert. Must not be {@code null}.
     * @return a hexadecimal string representation of the byte array, trimmed of trailing whitespace.
     * @throws NullPointerException if {@code bytes} is {@code null}.
     */
    private static String bytesToHex(byte[] bytes) {
        if (bytes == null) {
            throw new NullPointerException("bytes cannot be null");
        }

        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02X", b));
            sb.append(" ");
        }
        return sb.toString().trim();
    }
}