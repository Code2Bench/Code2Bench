public class Tested {
    /**
     * Converts a byte array into a hexadecimal string representation, with each byte separated by a colon.
     * Each byte is converted to a two-digit hexadecimal value. If the hexadecimal representation of a byte
     * is a single digit, a leading zero is added. The resulting string is converted to uppercase.
     *
     * @param b the byte array to convert; must not be null
     * @return a hexadecimal string representation of the byte array, with bytes separated by colons
     * @throws NullPointerException if the input byte array is null
     */
    public static String byte2hexSplitWithColon(byte[] b) {
        if (b == null) {
            throw new NullPointerException("Input byte array cannot be null");
        }

        StringBuilder result = new StringBuilder();
        for (byte bByte : b) {
            int hexValue = bByte & 0xFF;
            String hex = String.format("%02X", hexValue);
            result.append(hex).append(":");
        }
        return result.toString().substring(0, result.length() - 1);
    }
}