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
        // TODO: implement this method
    }
}