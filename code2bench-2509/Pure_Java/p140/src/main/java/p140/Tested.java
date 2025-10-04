package p140;

import java.util.regex.Pattern;

public class Tested {
    /**
     * Escapes special characters in the input string by replacing them with underscores or other
     * specified characters. The following transformations are applied:
     * <ul>
     *   <li>Characters '.', '/', ';', '$', ' ', ',', and '<' are replaced with '_'.</li>
     *   <li>The character '[' is replaced with 'A'.</li>
     *   <li>Characters ']', '>', '?', and '*' are removed from the string.</li>
     *   <li>All other characters are preserved as-is.</li>
     * </ul>
     *
     * @param str the input string to be escaped. Must not be null.
     * @return a new string with the specified characters escaped or removed.
     * @throws NullPointerException if the input string is null.
     */
    public static String escape(String str) {
        if (str == null) {
            throw new NullPointerException("Input string cannot be null");
        }

        StringBuilder result = new StringBuilder();
        for (char c : str.toCharArray()) {
            switch (c) {
                case '.': result.append('_'); break;
                case '/': result.append('_'); break;
                case ';': result.append('_'); break;
                case '$': result.append('_'); break;
                case ' ': result.append('_'); break;
                case ',': result.append('_'); break;
                case '<': result.append('_'); break;
                case '[': result.append('A'); break;
                case ']': result.deleteCharAt(result.length() - 1); break;
                case '>': result.deleteCharAt(result.length() - 1); break;
                case '?': result.deleteCharAt(result.length() - 1); break;
                case '*': result.deleteCharAt(result.length() - 1); break;
                default: result.append(c);
            }
        }
        return result.toString();
    }
}