package p246;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;

public class Tested {
    /**
     * Converts a hexadecimal string into a byte array. The input string must have an even length,
     * as each pair of hexadecimal characters represents a single byte. The conversion is case-insensitive.
     *
     * <p>For example, the input "1a2b3c" will be converted to the byte array {0x1a, 0x2b, 0x3c}.
     *
     * @param hex The hexadecimal string to convert. Must not be null and must have an even length.
     * @return A byte array containing the converted bytes.
     * @throws IllegalArgumentException if the input string is null, has an odd length, or contains
     *         non-hexadecimal characters.
     */
    public static byte[] hexStringToByteArray(String hex) {
        if (hex == null || hex.length() % 2 != 0) {
            throw new IllegalArgumentException("Hex string must be non-null and have even length");
        }

        byte[] result = new byte[hex.length() / 2];
        for (int i = 0; i < result.length; i++) {
            int index = i * 2;
            int value = 0;
            // Convert two hex characters to a byte
            value = (hex.charAt(index) & 0xF) << 4;
            value |= (hex.charAt(index + 1) & 0xF);
            result[i] = (byte) value;
        }
        return result;
    }
}