package p83;

import java.util.Objects;

public class Tested {
    /**
     * Finds the starting index of the line in the given text content, starting from the specified index.
     * The method searches backward from the start index to locate the nearest newline character (either '\n' or '\r').
     * The returned index is the position immediately after the newline character, or 0 if no newline is found.
     *
     * @param startIdx The index from which to start searching backward. Must be non-negative and less than or equal to the length of the text content.
     * @param textContent The text content to search within. Must not be null.
     * @return The index of the start of the line, which is the position after the nearest newline character or 0 if no newline is found.
     * @throws NullPointerException if {@code textContent} is null.
     * @throws IndexOutOfBoundsException if {@code startIdx} is negative or greater than the length of {@code textContent}.
     */
    public static int findLineStartIdx(int startIdx, String textContent) {
        // TODO: implement this method
    }
}