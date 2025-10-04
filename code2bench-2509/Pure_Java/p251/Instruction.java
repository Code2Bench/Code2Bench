package p251;

import java.util.Objects;

public class Tested {
    /**
     * Escapes special characters in the given text to make it safe for use in Lua strings.
     * Specifically, this method:
     * <ul>
     *   <li>Replaces backslashes (`\`) with double backslashes (`\\`).</li>
     *   <li>Escapes single quotes (`'`) with a backslash (`\'`).</li>
     *   <li>Escapes double quotes (`"`) with a backslash (`\"`).</li>
     *   <li>Replaces newlines (`\n`), carriage returns (`\r`), and tabs (`\t`) with spaces (` `).</li>
     * </ul>
     * If the input text is {@code null}, an empty string is returned.
     *
     * @param text the text to escape, may be {@code null}.
     * @return the escaped text, or an empty string if the input is {@code null}.
     */
    public static String escapeForLua(String text) {
        // TODO: implement this method
    }
}