package p76;

import java.util.ArrayList;
import java.util.List;

public class Tested {
    /**
     * Converts a hexadecimal string into a binary byte array. The input string must consist of an even number of
     * hexadecimal characters, where each pair of characters represents a single byte. The conversion is performed
     * by parsing each pair of characters as a hexadecimal value and storing the result in the corresponding byte
     * in the output array.
     *
     * @param hex The hexadecimal string to convert. Must not be null and must have an even length. Each character
     *            must be a valid hexadecimal digit (0-9, a-f, A-F).
     * @return A byte array containing the binary representation of the hexadecimal string.
     * @throws IllegalArgumentException if the input string is null, has an odd length, or contains invalid
     *                                  hexadecimal characters.
     * @throws NumberFormatException if any pair of characters cannot be parsed as a valid hexadecimal value.
     */
    public static byte[] hexToBinary(String hex) {
        if (hex == null || hex.length() % 2 != 0) {
            throw new IllegalArgumentException("Hexadecimal string must be non-null and have even length");
        }

        List<Byte> byteArray = new ArrayList<>();
        
        for (int i = 0; i < hex.length(); i += 2) {
            String pair = hex.substring(i, i + 2);
            try {
                byte value = Byte.parseByte(pair, 16);
                byteArray.add(value);
            } catch (NumberFormatException e) {
                throw new IllegalArgumentException("Invalid hexadecimal character: " + pair);
            }
        }

        return byteArray.toArray(new Byte[0]);
    }
}