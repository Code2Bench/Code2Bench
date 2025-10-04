public class Tested {
    /**
     * Converts a byte array into a hexadecimal string representation. Each byte is converted to a two-digit
     * hexadecimal value. If the hexadecimal representation of a byte is a single digit, a leading zero is
     * appended to ensure it is two digits long.
     *
     * @param bytes The byte array to convert. Must not be null.
     * @return A string representing the hexadecimal values of the bytes in the array. Returns an empty string
     *         if the input array is empty.
     * @throws NullPointerException if the input byte array is null.
     */
    public static String hexString(byte[] bytes) {
        if (bytes == null || bytes.length == 0) {
            return "";
        }

        StringBuilder result = new StringBuilder();
        for (byte b : bytes) {
            result.append(String.format("%02X", b));
        }
        return result.toString();
    }
}