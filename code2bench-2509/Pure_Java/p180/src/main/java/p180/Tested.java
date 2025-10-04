package p180;

import java.util.HashMap;
import java.util.Map;

public class Tested {
    /**
     * Filters the input string by replacing specific characters with their corresponding HTML/XML entities.
     * The method handles the following character replacements:
     * <ul>
     *   <li>'<' → "&lt;"</li>
     *   <li>'>' → "&gt;"</li>
     *   <li>'"' → "&quot;"</li>
     *   <li>'\' → "&#39;"</li>
     *   <li>'%' → "&#37;"</li>
     *   <li>';' → "&#59;"</li>
     *   <li>'(' → "&#40;"</li>
     *   <li>')' → "&#41;"</li>
     *   <li>'&' → "&amp;"</li>
     *   <li>'+' → "&#43;"</li>
     * </ul>
     * If the input string is {@code null}, the method returns {@code null}.
     *
     * @param value the input string to filter, may be {@code null}
     * @return the filtered string with special characters replaced by their HTML/XML entities, or {@code null} if the input is {@code null}
     */
    public static String filter(String value) {
        if (value == null) {
            return null;
        }

        Map<Character, String> entityMap = new HashMap<>();
        entityMap.put('<', "&lt;");
        entityMap.put('>', "&gt;");
        entityMap.put('"', "&quot;");
        entityMap.put('\'', "&#39;");
        entityMap.put('%', "&#37;");
        entityMap.put(';', "&#59;");
        entityMap.put('(', "&#40;");
        entityMap.put(")", "&#41;");
        entityMap.put('&', "&amp;");
        entityMap.put('+', "&#43;");

        StringBuilder result = new StringBuilder();
        for (char c : value.toCharArray()) {
            String entity = entityMap.get(c);
            if (entity != null) {
                result.append(entity);
            } else {
                result.append(c);
            }
        }
        return result.toString();
    }
}