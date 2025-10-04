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
        if (input == null) {
            return "";
        }

        // Remove invalid characters
        StringBuilder sanitized = new StringBuilder();
        for (char c : input.toCharArray()) {
            if (isValidChar(c)) {
                sanitized.append(c);
            }
        }

        // Remove control characters
        sanitized.replace(0, sanitized.length(), sanitized.toString().replaceAll("[\\u0000-\\u001F]", ""));

        // Collapse whitespace
        String trimmed = sanitized.toString().trim();
        return trimmed.replaceAll("\\s+", " ");
    }

    private static boolean isValidChar(char c) {
        // Check if character is valid (not a control character or one of the invalid ones)
        return !isControlCharacter(c) && !isInvalidFileChar(c);
    }

    private static boolean isControlCharacter(char c) {
        return c < 32 || c >= 127;
    }

    private static boolean isInvalidFileChar(char c) {
        // Invalid file characters: \, /, :, *, ?, ", <, >, |
        return c == '\\' || c == '/' || c == ':' || c == '*' || c == '?' || c == '"' || c == '<' || c == '>' || c == '|';
    }
}