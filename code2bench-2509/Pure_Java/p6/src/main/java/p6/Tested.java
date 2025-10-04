package p6;

import java.util.*;

public class Tested {
    /**
     * Determines whether a given position in a JSON string is within a quoted string.
     * This method iterates through the string up to the specified position, tracking whether
     * the current character is within a string literal by checking for unescaped double quotes.
     * It also handles escaped characters (e.g., backslashes) to ensure accurate detection.
     *
     * @param jsonStr the JSON string to analyze. Must not be null.
     * @param pos the position in the string to check. Must be a valid index within the string.
     * @return {@code true} if the position is within a quoted string, {@code false} otherwise.
     * @throws NullPointerException if {@code jsonStr} is null.
     * @throws IndexOutOfBoundsException if {@code pos} is out of bounds for {@code jsonStr}.
     */
    public static boolean isWithinString(String jsonStr, int pos) {
        if (jsonStr == null) {
            throw new NullPointerException("jsonStr cannot be null");
        }
        if (pos < 0 || pos >= jsonStr.length()) {
            throw new IndexOutOfBoundsException("pos is out of bounds for jsonStr");
        }

        int balance = 0;
        for (int i = 0; i <= pos; i++) {
            char c = jsonStr.charAt(i);
            if (c == '"') {
                balance++;
            } else if (c == '\\' && balance > 0) {
                // Skip escaped quote
                balance--;
            }
        }
        return balance > 0;
    }
}