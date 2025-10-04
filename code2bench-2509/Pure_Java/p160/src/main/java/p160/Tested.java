package p160;

import java.util.Objects;

public class Tested {
    /**
     * Escapes special characters in the given string to their corresponding HTML entities.
     * Specifically, the following characters are escaped:
     * <ul>
     *   <li>'&amp;' is replaced with "&amp;amp;"</li>
     *   <li>'&lt;' is replaced with "&amp;lt;"</li>
     *   <li>'&gt;' is replaced with "&amp;gt;"</li>
     *   <li>'&quot;' is replaced with "&amp;quot;"</li>
     * </ul>
     * All other characters are appended to the result unchanged.
     *
     * @param string the string to escape; may be null
     * @return the escaped string, or null if the input string is null
     */
    public static String escape(String string) {
        if (string == null) {
            return null;
        }
        
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < string.length(); i++) {
            char c = string.charAt(i);
            if (c == '&') {
                // Handle the & character
                switch (i + 1) {
                    case 1:
                        result.append("&amp;");
                        i++; // Skip the next character
                        break;
                    case 2:
                        result.append("&lt;");
                        i += 2;
                        break;
                    case 3:
                        result.append("&gt;");
                        i += 2;
                        break;
                    case 4:
                        result.append("&quot;");
                        i += 4;
                        break;
                    default:
                        result.append(c);
                        i++;
                        break;
                }
            } else {
                result.append(c);
            }
        }
        return result.toString();
    }
}