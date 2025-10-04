package p94;

import java.util.Objects;

public class Tested {
    /**
     * Converts a byte array into a hexadecimal string representation. Each byte is converted to a two-digit
     * hexadecimal value. If the hexadecimal representation of a byte is a single digit, a leading zero is
     * appended to ensure it is two digits long.
     *
     * @param hash The byte array to be converted. Must not be null.
     * @return A string representing the hexadecimal value of the byte array.
     * @throws NullPointerException if the input byte array is null.
     */
    public static String bytesToHex(byte[] hash) {
        if (hash == null) {
            throw new NullPointerException("Input byte array cannot be null");
        }

        StringBuilder hexString = new StringBuilder();
        for (byte b : hash) {
            int temp = b & 0xFF; // Ensure it's within 0-255
            hexString.append(String.format("%02X", temp));
        }
        return hexString.toString();
    }
}