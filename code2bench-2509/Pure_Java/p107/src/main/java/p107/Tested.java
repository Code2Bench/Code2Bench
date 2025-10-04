package p107;

import java.util.Objects;

public class Tested {
    /**
     * Determines whether the given string represents a valid integer. A valid integer consists
     * solely of one or more digits (0-9). The string must not be empty.
     *
     * @param s the string to check for integer validity; must not be null.
     * @return {@code true} if the string is a valid integer, {@code false} otherwise.
     * @throws NullPointerException if the input string is null.
     */
    public static boolean isInteger(String s) {
        if (s == null) {
            throw new NullPointerException("Input string cannot be null");
        }
        if (s.isEmpty()) {
            return false;
        }
        for (char c : s.toCharArray()) {
            if (!Character.isDigit(c)) {
                return false;
            }
        }
        return true;
    }
}