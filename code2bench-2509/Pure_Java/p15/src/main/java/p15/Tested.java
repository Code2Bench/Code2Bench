package p15;

import java.util.Objects;

public class Tested {
    /**
     * Escapes special characters in a given object's string representation to make it safe for JSON.
     * The method handles null values by returning an empty string.
     *
     * @param value The object whose string representation needs to be escaped. Can be null.
     * @return A string with special characters escaped, or an empty string if the input is null.
     * @implNote This method is currently a TODO and is not yet implemented.
     */
    public static String escapeJsonString(Object value) {
        if (value == null) {
            return "";
        }
        
        StringBuilder escaped = new StringBuilder();
        String str = value.toString();
        
        for (int i = 0; i < str.length(); i++) {
            char c = str.charAt(i);
            if (c == '\\' || c == '"' || c == '{' || c == '}' || c == '[' || c == ']' || c == ',' || c == ':' || c == '!' || c == '?' || c == '(' || c == ')' || c == '-' || c == '=' || c == '/' || c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\f') {
                escaped.append("\\");
                escaped.append(c);
            } else {
                escaped.append(c);
            }
        }
        
        return escaped.toString();
    }
}