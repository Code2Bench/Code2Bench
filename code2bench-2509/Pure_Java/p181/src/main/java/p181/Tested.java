public class Tested {
    /**
     * Converts a byte array into a hexadecimal string representation, with each byte separated by a colon.
     * Each byte is converted to a two-digit hexadecimal value. If the hexadecimal representation of a byte
     * is a single digit, it is prefixed with a '0'. The resulting string is returned in uppercase.
     *
     * @param b the byte array to convert. Must not be null.
     * @return a hexadecimal string representation of the byte array, with bytes separated by colons.
     * @throws NullPointerException if the input byte array {@code b} is null.
     */
    public static String byte2hex(byte[] b) {
        if (b == null) {
            throw new NullPointerException("Input byte array cannot be null");
        }

        StringBuilder result = new StringBuilder();
        for (byte bVal : b) {
            int hexValue = bVal & 0xFF; // Ensure it's within 0-255
            char firstChar = (char) ('0' + (hexValue / 16));
            char secondChar = (char) ('0' + (hexValue % 16));
            result.append(firstChar).append(secondChar);
        }
        return result.toString();
    }
}