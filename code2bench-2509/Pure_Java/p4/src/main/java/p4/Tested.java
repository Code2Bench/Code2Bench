package p4;

import java.util.Objects;

public class Tested {
    /**
     * Repeats the given string a specified number of times and returns the concatenated result.
     *
     * <p>If the input string is {@code null}, it is treated as an empty string. If the count is zero
     * or negative, an empty string is returned.
     *
     * @param value the string to repeat; may be {@code null}
     * @param count the number of times to repeat the string; if zero or negative, an empty string is returned
     * @return a new string consisting of the input string repeated {@code count} times; never {@code null}
     */
    public static String repeat(String value, int count) {
        if (count <= 0) {
            return "";
        }
        
        if (value == null) {
            return "";
        }
        
        return String.join("", Collections.nCopies(count, value));
    }
}