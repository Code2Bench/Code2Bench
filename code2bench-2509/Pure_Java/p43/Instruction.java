package p43;

import java.util.Objects;

public class Tested {
    /**
     * Converts a byte array into a hexadecimal string representation. Each byte in the array
     * is converted to a two-digit hexadecimal value. The conversion ensures that each byte
     * is treated as an unsigned value (0-255) and is padded with leading zeros if necessary.
     *
     * <p>For example, a byte array containing the values {@code {0x1A, 0x2B, (byte) 0xFF}} would
     * be converted to the string {@code "1a2bff"}.
     *
     * @param digest The byte array to be converted to a hexadecimal string. Must not be null.
     * @return A hexadecimal string representation of the byte array. The string will be
     *         lowercase and will have a length of twice the input array's length.
     * @throws NullPointerException if {@code digest} is null.
     */
    public static String encodeHex(byte[] digest) {
        // TODO: implement this method
    }
}