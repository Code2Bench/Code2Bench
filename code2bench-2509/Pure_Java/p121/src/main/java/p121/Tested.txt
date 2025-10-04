package p121;

import java.util.Objects;

public class Tested {
    /**
     * Sanitizes the input string by removing or replacing characters that are not suitable for
     * certain contexts, such as file names or paths. Specifically, this method:
     * <ul>
     *   <li>Replaces null input with an empty string.</li>
     *   <li>Removes characters that are typically invalid in file names (e.g., \, /, :, *, ?, ", <, >, |).</li>
     *   <li>Removes all control characters (non-printable characters).</li>
     *   <li>Collapses sequences of whitespace characters into a single space.</li>
     *   <li>Trims leading and trailing whitespace from the result.</li>
     * </ul>
     *
     * @param input the string to sanitize; may be null
     * @return the sanitized string; an empty string if the input is null
     */
    public static String sanitize(String input) {
        // TODO: implement this method
    }
}