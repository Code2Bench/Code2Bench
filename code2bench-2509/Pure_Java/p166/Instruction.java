package p166;

import java.util.Objects;

public class Tested {
    /**
     * Removes all SQL-style comments from the provided SQL string while preserving string literals.
     * This method handles both single-line comments (starting with '--') and block comments (enclosed in '/*' and '*\/').
     * String literals enclosed in single quotes (') or double quotes (") are preserved and not processed for comments.
     *
     * <p>The method processes the input string character by character, maintaining state flags to track whether
     * it is inside a single-line comment, block comment, single-quoted string, or double-quoted string. Characters
     * inside comments are skipped, while characters outside comments and inside string literals are appended to the
     * output.
     *
     * @param sql The SQL string from which comments should be stripped. Must not be null.
     * @return A new string with all comments removed, preserving string literals and other content.
     * @throws NullPointerException if the input SQL string is null.
     */
    public static String stripComments(String sql) {
        // TODO: implement this method
    }
}