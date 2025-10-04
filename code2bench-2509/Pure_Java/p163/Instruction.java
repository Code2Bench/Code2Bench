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
        // TODO: implement this method
    }
}