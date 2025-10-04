package p176;

import java.util.regex.Pattern;

public class Tested {
    /**
     * Removes single quotes from the beginning and end of the given string, if present. Additionally,
     * replaces any occurrences of two consecutive single quotes ('') within the string with a single
     * quote ('). If the string is null, does not start and end with a single quote, or is too short
     * to contain both quotes, the original string is returned unchanged.
     *
     * @param value The string to unquote. May be null or empty.
     * @return The unquoted string, or the original string if no quotes were removed.
     */
    private static String unquote(String value) {
        if (value == null) {
            return value;
        }

        // Remove leading and trailing single quotes
        String cleaned = value.replaceAll("^'[^']*'$", "");
        cleaned = cleaned.replaceAll("'$[^']*'", "");

        // Replace two consecutive single quotes with a single one
        cleaned = cleaned.replaceAll("''", "'");

        return cleaned;
    }
}