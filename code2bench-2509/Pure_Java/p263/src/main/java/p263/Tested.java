package p263;

import java.util.ArrayList;
import java.util.List;

public class Tested {
    /**
     * Converts a given string into a "safe" representation by replacing non-printable or non-ASCII
     * characters with their corresponding integer values enclosed in angle brackets. Printable ASCII
     * characters (those with values between 32 and 127, inclusive) are preserved as-is.
     *
     * <p>For example, the string "Hello\u0009World!" would be converted to "Hello&lt;9&gt;World!".
     *
     * @param src The input string to be processed. If {@code null}, the behavior is undefined
     *            (the method does not explicitly handle null inputs).
     * @return A new string where non-printable or non-ASCII characters are replaced with their
     *         integer representations enclosed in angle brackets.
     */
    private static String safe(String src) {
        if (src == null) {
            return null;
        }

        StringBuilder result = new StringBuilder();
        for (int i = 0; i < src.length(); i++) {
            char c = src.charAt(i);
            if (c >= ' ' && c <= '~') {
                result.append(c);
            } else {
                result.append("<").append(Integer.toHexString(c & 0xFF)).append(">"); // Use hex for non-ASCII
            }
        }
        return result.toString();
    }
}