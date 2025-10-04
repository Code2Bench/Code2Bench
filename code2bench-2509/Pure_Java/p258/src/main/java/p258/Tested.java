package p258;

import java.nio.charset.StandardCharsets;

public class Tested {
    /**
     * Converts a given string into a byte array where each character in the string is cast to a byte.
     * The resulting byte array has the same length as the input string, and each byte corresponds
     * to the ASCII value of the character at the same position in the string.
     *
     * <p>This method does not handle characters outside the ASCII range (0-127) correctly, as casting
     * a char to a byte will truncate values outside this range.
     *
     * @param basicString the string to convert to a byte array. Must not be null.
     * @return a byte array representing the input string, where each byte is the ASCII value of the
     *         corresponding character in the string.
     * @throws NullPointerException if {@code basicString} is null.
     */
    public static byte[] asBytes(String basicString) {
        if (basicString == null) {
            throw new NullPointerException("basicString cannot be null");
        }
        
        byte[] byteArray = new byte[basicString.length()];
        for (int i = 0; i < basicString.length(); i++) {
            byteArray[i] = (byte) basicString.charAt(i);
        }
        return byteArray;
    }
}