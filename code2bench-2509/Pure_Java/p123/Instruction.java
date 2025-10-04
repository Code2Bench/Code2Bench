package p123;

import java.util.Objects;

public class Tested {
    /**
     * Cleans a number format string by removing specific characters and handling special cases.
     * The method processes the input string to remove:
     * <ul>
     *   <li>Spacers ('_') and full-column-width padding ('*') characters, unless they are escaped with a backslash.</li>
     *   <li>Quotes ('"') and backslashes ('\').</li>
     *   <li>The '+' sign in scientific/engineering notation (e.g., 'E+').</li>
     * </ul>
     * The method iterates through the string twice: first to handle spacers and padding, and second to handle quotes,
     * backslashes, and scientific notation.
     *
     * @param formatStr The format string to clean. Must not be null.
     * @return The cleaned format string, with the specified characters removed.
     * @throws NullPointerException if {@code formatStr} is null.
     */
    public static String cleanFormatForNumber(String formatStr) {
        // TODO: implement this method
    }
}