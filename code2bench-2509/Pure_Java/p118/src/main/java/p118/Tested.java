package p118;

import java.util.Objects;

public class Tested {
    /**
     * Determines if the given executable string is safe to execute based on a set of allowed characters.
     * The method checks if the executable string is non-null, non-blank, and contains only allowed characters.
     * Allowed characters include word characters (letters, digits, and underscores), dots, forward slashes,
     * backslashes, and dashes. Spaces and shell metacharacters are not allowed.
     *
     * @param exec the executable string to check for safety, may be null or blank
     * @return {@code true} if the executable string is safe to execute, {@code false} otherwise
     */
    public static boolean isSafeExecutable(String exec) {
        if (exec == null || exec.isEmpty()) {
            return false;
        }

        char[] chars = exec.toCharArray();
        for (char c : chars) {
            if (!isAllowedCharacter(c)) {
                return false;
            }
        }
        return true;
    }

    private static boolean isAllowedCharacter(char c) {
        // Allow word characters (letters, digits, underscores)
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '_') {
            return true;
        }
        // Allow dots, forward slashes, backslashes, and dashes
        if (c == '.' || c == '/' || c == '\\' || c == '-') {
            return true;
        }
        // Disallow spaces and shell metacharacters
        if (c == ' ') {
            return false;
        }
        return false;
    }
}