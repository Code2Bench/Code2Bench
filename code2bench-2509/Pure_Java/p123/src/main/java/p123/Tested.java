package p123;

import java.util.Objects;

public class Tested {
    /**
     * Cleans a number format string by removing specific characters and handling special cases.
     * The method processes the input string to remove:
     * <ul>
     *   <li>Spacers ('_') and full-column-width padding ('*') characters, unless they are escaped with a backslash.</li>
     *   <li>Quotes ('"') and backslashes ('\').</li>
     *   <li>The '+' sign in scientific/engineering notation (e.g., 'E+').</li>
     * </ul>
     * The method iterates through the string twice: first to handle spacers and padding, and second to handle quotes,
     * backslashes, and scientific notation.
     *
     * @param formatStr The format string to clean. Must not be null.
     * @return The cleaned format string, with the specified characters removed.
     * @throws NullPointerException if {@code formatStr} is null.
     */
    public static String cleanFormatForNumber(String formatStr) {
        if (formatStr == null) {
            throw new NullPointerException("formatStr cannot be null");
        }

        StringBuilder cleaned = new StringBuilder();
        int i = 0;
        int n = formatStr.length();

        // First pass: remove spacers and padding
        while (i < n) {
            char c = formatStr.charAt(i);
            if (c == '_' || c == '*' || (c == '\\' && i + 1 < n && formatStr.charAt(i + 1) == '*')) {
                i++;
            } else {
                cleaned.append(c);
                i++;
            }
        }

        // Second pass: remove quotes and backslashes, and handle scientific notation
        i = 0;
        while (i < n) {
            char c = formatStr.charAt(i);
            if (c == '"' || c == '\\') {
                i++;
            } else if (c == '+' && i + 1 < n && formatStr.charAt(i + 1) == 'E') {
                i += 2;
            } else {
                cleaned.append(c);
                i++;
            }
        }

        return cleaned.toString();
    }
}