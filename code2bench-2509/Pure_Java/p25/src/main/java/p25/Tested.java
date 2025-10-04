public class Tested {
    /**
     * Converts a byte array into a hexadecimal string representation. Each byte is converted to a two-digit
     * hexadecimal value. If the input byte array is null or empty, this method returns null.
     *
     * <p>For example, the byte array {@code {0x1A, 0x2B}} will be converted to the string {@code "1a2b"}.
     *
     * @param src the byte array to convert, may be null or empty
     * @return a hexadecimal string representation of the byte array, or null if the input is null or empty
     */
    public static String bytesToHexString(byte[] src) {
        if (src == null || src.length == 0) {
            return null;
        }

        StringBuilder sb = new StringBuilder();
        for (byte b : src) {
            sb.append(String.format("%02X", b));
        }
        return sb.toString();
    }
}