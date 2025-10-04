package p271;

import java.util.Objects;

public class Tested {
    /**
     * Removes all occurrences of carriage return ('\r') and line feed ('\n') characters from the input string.
     * Each occurrence of '\n' or '\r' is replaced with a single space (' '). If a '\r' is followed by a '\n',
     * both characters are replaced with a single space to avoid double spacing.
     *
     * <p>If the input string does not contain any '\n' or '\r' characters, it is returned unchanged.
     *
     * @param text the input string from which to remove '\r' and '\n' characters. Must not be null.
     * @return a new string with all '\r' and '\n' characters replaced by spaces, or the original string if no
     *         such characters are present.
     * @throws NullPointerException if {@code text} is null.
     */
    public static String removeCRLF(String text) {
        // TODO: implement this method
    }
}