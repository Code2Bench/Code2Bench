package p256;

import java.util.StringBuffer;

public class Tested {
    /**
     * Escapes characters in the given string that are not printable ASCII characters or newline characters.
     * Specifically, any character with a value less than 32 (non-printable control characters) or greater than
     * or equal to 127 (non-ASCII characters) is replaced with a question mark ('?'). Newline characters ('\n')
     * are preserved as is.
     *
     * @param msg the input string to be escaped. If {@code null}, the behavior is undefined (may throw {@code NullPointerException}).
     * @return a new string with non-printable and non-ASCII characters replaced by '?', and newline characters preserved.
     */
    public static String escape(String msg) {
        // TODO: implement this method
    }
}