package p143;

import java.util.Objects;

public class Tested {
    /**
     * Extracts a line of text from the given content string, based on the specified position and end index.
     * The method identifies the start and end of the line containing the position and returns the substring
     * representing the entire line. If the position is beyond the content length, an empty string is returned.
     * If the end index is not specified (i.e., -1), it defaults to the position + 1. If the end index exceeds
     * the content length, it is adjusted to the last character of the content.
     *
     * @param content The string from which to extract the line. Must not be null.
     * @param pos The position within the content to identify the line. Must be a non-negative integer.
     * @param end The end index to limit the search for the line end. Use -1 to default to position + 1.
     * @return The extracted line as a string. Returns an empty string if the position is beyond the content length.
     * @throws NullPointerException if the content is null.
     */
    public static String getLine(String content, int pos, int end) {
        // TODO: implement this method
    }
}