package p270;

import java.util.HashMap;
import java.util.Map;

public class Tested {
    /**
     * Escapes special characters in the given content to their corresponding HTML entities.
     * Specifically, the following characters are replaced:
     * <ul>
     *   <li>'&lt;' is replaced with "&lt;"</li>
     *   <li>'&gt;' is replaced with "&gt;"</li>
     *   <li>'\'' is replaced with "&apos;"</li>
     *   <li>'\"' is replaced with "&quot;"</li>
     *   <li>'&' is replaced with "&amp;"</li>
     * </ul>
     * All other characters are appended to the result unchanged.
     *
     * @param content the input string to be escaped. If null, the method returns null.
     * @return a new string with special characters escaped, or null if the input is null.
     */
    public static String escape(String content) {
        if (content == null) {
            return null;
        }

        StringBuilder result = new StringBuilder();
        Map<String, String> replacements = new HashMap<>();
        replacements.put("&lt;", "&lt;");
        replacements.put("&gt;", "&gt;");
        replacements.put("\'", "&apos;");
        replacements.put("&quot;", "&quot;");
        replacements.put("&", "&amp;");

        for (int i = 0; i < content.length(); i++) {
            char c = content.charAt(i);
            if (replacements.containsKey(String.valueOf(c))) {
                result.append(replacements.get(String.valueOf(c)));
            } else {
                result.append(c);
            }
        }

        return result.toString();
    }
}