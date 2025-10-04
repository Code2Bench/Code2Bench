package p234;

import java.util.*;

public class Tested {
    /**
     * Converts standalone 'y' characters in the input string to 'yyyy', while ignoring 'y' characters
     * that are part of a sequence of 'y's or are inside single quotes. This method is useful for
     * transforming specific patterns in strings, such as date formats.
     *
     * <p>For example:
     * <ul>
     *   <li>"y" → "yyyy"</li>
     *   <li>"yy" → "yy"</li>
     *   <li>"'y'" → "'y'"</li>
     *   <li>"y'y'" → "yyyy'y'"</li>
     * </ul>
     *
     * @param str the input string to process. If null, the behavior is undefined.
     * @return a new string with standalone 'y' characters replaced by 'yyyy'.
     */
    public static String y2yyyy(String str) {
        if (str == null) {
            return null;
        }

        StringBuilder result = new StringBuilder();
        int i = 0;

        while (i < str.length()) {
            if (str.charAt(i) == '\'' && i + 1 < str.length() && str.charAt(i + 1) == 'y') {
                // Inside single quote, skip 'y'
                i += 2;
            } else if (str.charAt(i) == 'y') {
                // Standalone 'y' -> 'yyyy'
                result.append("yyyy");
                i += 2;
            } else {
                // Regular character, add as is
                result.append(str.charAt(i));
                i++;
            }
        }

        return result.toString();
    }
}