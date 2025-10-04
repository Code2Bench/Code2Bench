public class Tested {
    /**
     * Converts a specified portion of a byte array into a String, treating each byte as a single character.
     * The method creates a new char array of the specified length, copies the bytes from the specified offset
     * into the char array, and then constructs a String from the char array.
     *
     * @param bytes The byte array from which to extract characters. Must not be null.
     * @param offset The starting position in the byte array from which to begin extraction. Must be non-negative.
     * @param length The number of bytes to extract and convert to characters. Must be non-negative.
     * @return A String constructed from the specified portion of the byte array.
     * @throws NullPointerException if {@code bytes} is null.
     * @throws IndexOutOfBoundsException if {@code offset} or {@code length} is negative, or if
     *         {@code offset + length} exceeds the length of the byte array.
     */
    public static String asBasicString(byte[] bytes, int offset, int length) {
        if (bytes == null) {
            throw new NullPointerException("bytes cannot be null");
        }
        if (offset < 0 || length < 0) {
            throw new IndexOutOfBoundsException("offset and length must be non-negative");
        }
        if (offset + length > bytes.length) {
            throw new IndexOutOfBoundsException("offset + length exceeds the length of the byte array");
        }
        
        char[] chars = new char[length];
        for (int i = 0; i < length; i++) {
            chars[i] = (char) bytes[offset + i];
        }
        return new String(chars);
    }
}