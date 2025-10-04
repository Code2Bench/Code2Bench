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
        if (content == null) {
            throw new NullPointerException("content cannot be null");
        }

        int contentLength = content.length();
        if (pos < 0) {
            throw new IllegalArgumentException("pos must be a non-negative integer");
        }

        // Default end index to position + 1 if not specified
        if (end == -1) {
            end = pos + 1;
        }

        // Ensure end does not exceed content length
        end = Math.min(end, contentLength);

        // Find the start of the line
        int start = pos;
        while (start < end && !Character.isWhitespace(content.charAt(start))) {
            start++;
        }

        // If start is still at pos, it means there is no whitespace before the line
        if (start == pos) {
            start = 0;
        }

        // Extract the line from start to end (inclusive)
        return content.substring(start, end);
    }
}