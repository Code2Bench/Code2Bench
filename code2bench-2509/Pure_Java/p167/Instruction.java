package p167;

import java.util.Objects;

public class Tested {
    /**
     * Formats a JSON string by escaping newline and tab characters inside quoted strings.
     * This method processes the input string character by character, tracking whether the current
     * character is inside a quoted string. If a newline or tab character is encountered inside
     * a quoted string, it is replaced with its escape sequence ("\\n" or "\\t"). Newline characters
     * outside quoted strings are removed.
     *
     * <p>This method assumes that the input string is a valid JSON string. It does not validate
     * the JSON structure.
     *
     * @param jstr The JSON string to format. Must not be null.
     * @return The formatted JSON string with escaped newline and tab characters inside quoted strings.
     * @throws NullPointerException if {@code jstr} is null.
     */
    public static String formatJsonStr(String jstr) {
        // TODO: implement this method
    }
}