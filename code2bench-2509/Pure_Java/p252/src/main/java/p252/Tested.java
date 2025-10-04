package p252;

import java.util.stream.Collectors;

public class Tested {
    /**
     * Converts an array of bytes into a hexadecimal string representation. Each byte is
     * formatted as a two-digit uppercase hexadecimal value, separated by a space.
     *
     * <p>For example, the byte array {@code {0x1A, 0x2B, 0x3C}} will be converted to the
     * string {@code "1A 2B 3C "}.
     *
     * @param bytes The array of bytes to convert. If {@code null}, the behavior is undefined
     *              (may throw {@code NullPointerException}).
     * @return A string representation of the bytes in hexadecimal format, with each byte
     *         separated by a space. If the input array is empty, an empty string is returned.
     */
    public static String bytesToHex(byte[] bytes) {
        if (bytes == null || bytes.length == 0) {
            return "";
        }

        return Arrays.stream(bytes)
                .map(byteValue -> String.format("%02X", byteValue))
                .collect(Collectors.joining(" "));
    }
}