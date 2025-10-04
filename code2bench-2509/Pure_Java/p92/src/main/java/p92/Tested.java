package p92;

import java.util.Objects;

public class Tested {
    /**
     * Pads the specified string on the right with the given character until the string reaches the specified total width.
     * If the string is already longer than or equal to the specified total width, it is returned unchanged.
     *
     * @param str The string to pad. If null, a {@code NullPointerException} will be thrown.
     * @param totalWidth The desired total width of the padded string. Must be non-negative.
     * @param padChar The character to use for padding.
     * @return A new string padded on the right with the specified character to the specified total width.
     * @throws IllegalArgumentException if {@code totalWidth} is negative.
     * @throws NullPointerException if {@code str} is null.
     */
    public static String padRight(String str, int totalWidth, char padChar) {
        if (totalWidth < 0) {
            throw new IllegalArgumentException("Total width must be non-negative");
        }
        if (str == null) {
            throw new NullPointerException("String cannot be null");
        }

        int length = str.length();
        if (length >= totalWidth) {
            return str;
        }

        int padding = totalWidth - length;
        StringBuilder sb = new StringBuilder(str);
        for (int i = 0; i < padding; i++) {
            sb.append(padChar);
        }
        return sb.toString();
    }
}