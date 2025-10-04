package p138;

import java.util.regex.Pattern;

public class Tested {
    /**
     * Cleans an object name by removing the leading 'L' and trailing ';' if present,
     * and replacing any '/' characters with '.'. If the input string does not start
     * with 'L' or does not end with ';', it is returned unchanged.
     *
     * @param obj The object name to clean. Must not be null and must have a length
     *            of at least 1 character.
     * @return The cleaned object name, or the original string if no cleaning was
     *         necessary.
     * @throws NullPointerException if {@code obj} is null.
     * @throws StringIndexOutOfBoundsException if {@code obj} is an empty string.
     */
    public static String cleanObjectName(String obj) {
        if (obj == null || obj.isEmpty()) {
            throw new StringIndexOutOfBoundsException("Object must have at least one character");
        }

        // Check if the string starts with 'L' and ends with ';'
        boolean startsWithL = obj.startsWith("L");
        boolean endsWithSemicolon = obj.endsWith(";");

        if (startsWithL && endsWithSemicolon) {
            // Remove leading 'L' and trailing ';'
            String cleaned = obj.substring(1).replaceAll("/\\.", ".");
            return cleaned;
        } else {
            return obj;
        }
    }
}