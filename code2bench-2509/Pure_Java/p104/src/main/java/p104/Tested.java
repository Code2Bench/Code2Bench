import java.lang.StringBuilder;

public class Tested {
    /**
     * Consumes characters from the specified string starting at the given cursor position until
     * the specified delimiter is encountered or the end of the string is reached. The consumed
     * characters are appended to the provided {@link StringBuilder}.
     *
     * <p>This method is useful for parsing unquoted segments of a string, such as in CSV or
     * delimiter-separated value parsing.
     *
     * @param string    the string from which characters are consumed. Must not be null.
     * @param delimiter the character that marks the end of the segment to consume. Must not be null.
     * @param cursor    the starting position in the string from which to begin consuming characters.
     *                  Must be a valid index within the bounds of the string.
     * @param builder   the {@link StringBuilder} to which the consumed characters are appended.
     *                  Must not be null.
     * @return the index of the delimiter if it is encountered, or the length of the string if the
     *         end of the string is reached.
     * @throws NullPointerException if {@code string}, {@code delimiter}, or {@code builder} is null.
     * @throws IndexOutOfBoundsException if {@code cursor} is out of bounds for the string.
     */
    private static int consumeUnquoted(
            String string, char delimiter, int cursor, StringBuilder builder) {
        int index = cursor;
        while (index < string.length()) {
            if (string.charAt(index) == delimiter) {
                builder.append(string.substring(cursor, index));
                return index;
            }
            index++;
        }
        builder.append(string.substring(cursor));
        return string.length();
    }
}