package p269;

import java.io.UnsupportedEncodingException;

public class Tested {
    /**
     * Converts a UTF-32 code point into its corresponding UTF-16 encoded string.
     *
     * <p>This method handles both BMP (Basic Multilingual Plane) and supplementary characters.
     * For BMP characters (code points less than 0x10000), the method directly converts the code point
     * to a single UTF-16 character. For supplementary characters (code points greater than or equal to 0x10000),
     * the method converts the code point into a surrogate pair, which consists of two UTF-16 characters.
     *
     * @param codePoint the UTF-32 code point to convert. Must be a valid Unicode code point.
     * @return a string representing the UTF-16 encoded character(s) corresponding to the given code point.
     * @throws IllegalArgumentException if the code point is not a valid Unicode code point.
     */
    public static String convertFromUtf32(int codePoint) {
        if (codePoint < 0 || codePoint >= 0x10000) {
            throw new IllegalArgumentException("Invalid code point");
        }

        if (codePoint < 0x10000) {
            return String.format("%c", (char) codePoint);
        } else {
            int high = (codePoint - 0x10000) / 0x400 + 0x10000;
            int low = (codePoint - 0x10000) % 0x400 + 0x800;
            return String.format("%c%c", (char) high, (char) low);
        }
    }
}