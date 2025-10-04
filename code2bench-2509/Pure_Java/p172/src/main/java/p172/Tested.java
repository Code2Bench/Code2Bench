package p172;

import java.util.Objects;

public class Tested {
    /**
     * Finds the index of the first special character (space or ISO control character) in the given
     * message, starting from the specified position. If no such character is found, returns -1.
     *
     * <p>Special characters are defined as:
     * <ul>
     *   <li>Space (' ')</li>
     *   <li>Any ISO control character (as determined by {@link Character#isISOControl(char)})</li>
     * </ul>
     *
     * @param message the string to search within. Must not be null.
     * @param pos the starting position for the search. Must be non-negative and less than the length
     *            of the message.
     * @return the index of the first special character found, or -1 if no such character exists in
     *         the message starting from the given position.
     * @throws NullPointerException if {@code message} is null.
     * @throws IndexOutOfBoundsException if {@code pos} is negative or greater than or equal to the
     *         length of the message.
     */
    private static int indexOfSpecial(String message, int pos) {
        if (message == null || pos < 0 || pos >= message.length()) {
            throw new IndexOutOfBoundsException("Invalid position");
        }

        while (pos < message.length()) {
            char c = message.charAt(pos);
            if (c == ' ' || Character.isISOControl(c)) {
                return pos;
            }
            pos++;
        }

        return -1;
    }
}