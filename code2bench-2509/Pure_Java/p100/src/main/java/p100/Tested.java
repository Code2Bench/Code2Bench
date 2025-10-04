package p100;

import java.util.Objects;

public class Tested {
    /**
     * Replaces invalid characters in the input string with valid alternatives or removes them entirely.
     * The method processes the input string character by character and applies the following rules:
     * - Characters '<', '>', and '"' are removed from the string.
     * - Spaces (' ') are replaced with underscores ('_').
     * - Characters ',', '=', ';', ':', '?', '\'', and '*' are replaced with hyphens ('-').
     * - All other characters are preserved as-is.
     *
     * If no invalid characters are found, the original string is returned without modification.
     *
     * @param str The input string to process. Must not be null.
     * @return A new string with invalid characters replaced or removed. If no replacements are needed,
     *         the original string is returned.
     * @throws NullPointerException if the input string is null.
     */
    public static String replaceInvalidChars(String str) {
        if (str == null) {
            throw new NullPointerException("Input string cannot be null");
        }

        StringBuilder result = new StringBuilder();
        for (char c : str.toCharArray()) {
            switch (c) {
                case '<':
                case '>':
                case '"':
                    break;
                case ' ':
                    result.append('_');
                    break;
                case ',':
                case '=':
                case ';':
                case ':':
                case '?':
                case '\'':
                case '*':
                    result.append('-');
                    break;
                default:
                    result.append(c);
            }
        }
        return result.toString();
    }
}