package p142;

import java.util.Objects;

public class Tested {
    /**
     * Counts the number of newline characters ('\n') in the specified content string between the
     * given start position and the specified position (exclusive). If the start position is greater
     * than or equal to the specified position, the method returns 0. The search begins at the start
     * position and continues until the specified position is reached or the end of the content is
     * encountered.
     *
     * @param content the string to search for newline characters. Must not be null.
     * @param pos the position in the content string up to which newline characters are counted
     *            (exclusive). Must be a valid index within the content string.
     * @param start the position in the content string from which to start counting newline
     *              characters. Must be a valid index within the content string.
     * @return the number of newline characters found between the start position and the specified
     *         position (exclusive).
     * @throws NullPointerException if the content string is null.
     * @throws IndexOutOfBoundsException if either pos or start is out of bounds for the content
     *         string.
     */
    public static int countLinesByPos(String content, int pos, int start) {
        // TODO: implement this method
    }
}