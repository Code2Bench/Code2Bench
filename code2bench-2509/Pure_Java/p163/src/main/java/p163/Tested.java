package p163;

import java.util.Objects;

public class Tested {
    /**
     * Escapes special characters in the given string and wraps it in double quotes. The method handles
     * the following special characters:
     * <ul>
     *   <li>Single quote (') is escaped as \\'</li>
     *   <li>Double quote (") is escaped as \\"</li>
     *   <li>Carriage return (\r) is escaped as \\r</li>
     *   <li>Newline (\n) is escaped as \\n</li>
     *   <li>Tab (\t) is escaped as \\t</li>
     *   <li>Non-printable characters (ASCII < 32 or >= 127) are escaped as \\uXXXX, where XXXX is the
     *       Unicode code point in hexadecimal format.</li>
     * </ul>
     * The resulting string is enclosed in double quotes.
     *
     * @param value the string to escape. Must not be null.
     * @return the escaped string, wrapped in double quotes.
     * @throws NullPointerException if the input string is null.
     */
    public static String escape(String value) {
        if (value == null) {
            throw new NullPointerException("Input string cannot be null");
        }

        StringBuilder result = new StringBuilder();
        int length = value.length();

        for (int i = 0; i < length; i++) {
            char c = value.charAt(i);

            if (c == '\'') {
                result.append("\\'"); // Escape single quote
            } else if (c == '"') {
                result.append("\\\""); // Escape double quote
            } else if (c == '\r') {
                result.append("\\r"); // Escape carriage return
            } else if (c == '\n') {
                result.append("\\n"); // Escape newline
            } else if (c == '\t') {
                result.append("\\t"); // Escape tab
            } else {
                // Handle non-printable characters
                int codePoint = c;
                if (codePoint < 32 || codePoint >= 127) {
                    result.append("\\u" + Integer.toHexString(codePoint & 0xFFFF));
                } else {
                    result.append(c);
                }
            }
        }

        return "\"" + result.toString() + "\"";
    }
}