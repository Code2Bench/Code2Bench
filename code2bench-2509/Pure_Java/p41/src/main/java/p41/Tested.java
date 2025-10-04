public class Tested {
    /**
     * Converts a byte array into a hexadecimal string representation. Each byte is converted
     * to two hexadecimal characters, using lowercase letters (0-9, a-f). The conversion is
     * performed by mapping each nibble (4 bits) of the byte to its corresponding hexadecimal
     * character.
     *
     * <p>For example, the byte array {@code [0x1A, 0x2B]} will be converted to the string
     * {@code "1a2b"}.
     *
     * @param hash The byte array to convert. Must not be null, but can be empty. If empty,
     *             an empty string is returned.
     * @return A hexadecimal string representation of the input byte array. The string will
     *         be empty if the input array is empty.
     * @throws NullPointerException if {@code hash} is {@code null}.
     */
    public static String bytesToHex(byte[] hash) {
        if (hash == null) {
            throw new NullPointerException("hash cannot be null");
        }
        
        StringBuilder hexString = new StringBuilder();
        for (byte b : hash) {
            int high = (b >> 4) & 0xF;
            int low = b & 0xF;
            hexString.append(String.format("%02X", high));
            hexString.append(String.format("%02X", low));
        }
        
        return hexString.toString();
    }
}