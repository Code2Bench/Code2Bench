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
        if (sql == null) {
            throw new NullPointerException("Input SQL string cannot be null");
        }

        int n = sql.length();
        StringBuilder result = new StringBuilder();
        boolean inSingleLineComment = false;
        boolean inBlockComment = false;
        boolean inSingleQuote = false;
        boolean inDoubleQuote = false;

        for (int i = 0; i < n; i++) {
            char c = sql.charAt(i);

            if (inSingleLineComment || inBlockComment) {
                // Skip comments
                result.append(c);
                continue;
            }

            if (inSingleQuote) {
                // Inside single-quoted string, skip comment processing
                result.append(c);
                continue;
            }

            if (inDoubleQuote) {
                // Inside double-quoted string, skip comment processing
                result.append(c);
                continue;
            }

            // Check for single-line comment
            if (c == '-') {
                if (i + 1 < n && sql.charAt(i + 1) == '*') {
                    inSingleLineComment = true;
                } else if (i + 1 < n && sql.charAt(i + 1) == '/') {
                    // Single-line comment ends at first '/' after '-'
                    inSingleLineComment = true;
                }
            }

            // Check for block comment
            if (c == '/' && i + 1 < n && sql.charAt(i + 1) == '*') {
                inBlockComment = true;
            }

            // Check for string literals
            if (c == '\'' || c == '"') {
                inSingleQuote = (c == '\'');
                inDoubleQuote = (c == '"');
            } else {
                result.append(c);
            }
        }

        return result.toString();
    }
}