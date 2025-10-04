package p165;

import java.util.ArrayList;
import java.util.List;

public class Tested {
    /**
     * Escapes special characters in the given string. Specifically, double quotes (`"`), newline (`\n`),
     * and carriage return (`\r`) characters are replaced with their escaped counterparts (`\\"`, `\\n`, `\\r`).
     * If the input string is {@code null}, an empty string is returned.
     *
     * @param str the string to escape; may be {@code null}
     * @return the escaped string, or an empty string if the input is {@code null}
     */
    public static String escapeString(String str) {
        if (str == null) {
            return "";
        }
        
        StringBuilder escaped = new StringBuilder();
        for (int i = 0; i < str.length(); i++) {
            char c = str.charAt(i);
            switch (c) {
                case '"':
                    escaped.append("\\\"");
                    break;
                case '\n':
                    escaped.append("\\n");
                    break;
                case '\r':
                    escaped.append("\\r");
                    break;
                default:
                    escaped.append(c);
                    break;
            }
        }
        return escaped.toString();
    }
}