public class Tested {
    /**
     * Offsets each byte in the given string by the specified amount and returns the resulting string.
     * The method converts the input string to a byte array using the platform's default charset,
     * increments each byte by the offset value, and then constructs a new string from the modified byte array.
     *
     * <p>If the input string is {@code null}, the method will throw a {@link NullPointerException}.
     * The offset can be positive or negative, and the method handles overflow/underflow of byte values
     * by wrapping around within the byte range (-128 to 127).
     *
     * @param msg the input string to be offset; must not be {@code null}
     * @param o the amount to offset each byte in the string
     * @return a new string constructed from the offset byte array
     * @throws NullPointerException if the input string {@code msg} is {@code null}
     */
    public static String offset(String msg, int o) {
        if (msg == null) {
            throw new NullPointerException("Input string cannot be null");
        }

        byte[] bytes = msg.getBytes(StandardCharsets.UTF_8);
        int offsetValue = o % 256; // Ensure it's within 0-255

        for (int i = 0; i < bytes.length; i++) {
            bytes[i] = (byte) ((bytes[i] + offsetValue) % 256);
        }

        return new String(bytes);
    }
}