package p7;

import java.util.Objects;

public class Tested {
    /**
     * Removes trailing commas in a JSON string that appear before closing braces (`}`) or
     * brackets (`]`). This method processes the input string character by character,
     * deleting any comma that is immediately followed by a closing brace or bracket.
     *
     * <p>For example, given the input string `{"key": "value",}`, this method will return
     * `{"key": "value"}`. Similarly, `[1, 2, 3,]` will be transformed into `[1, 2, 3]`.
     *
     * <p>If the input string is `null`, this method returns `null`. If the input string is
     * empty, it is returned as-is.
     *
     * @param jsonStr the JSON string to process, which may contain trailing commas.
     * @return the processed JSON string with trailing commas removed, or `null` if the
     *         input is `null`.
     */
    public static String handleTrailingCommas(String jsonStr) {
        if (jsonStr == null) {
            return null;
        }
        
        if (jsonStr.isEmpty()) {
            return jsonStr;
        }
        
        int n = jsonStr.length();
        int i = n - 1;
        
        // Traverse from the end to find the last comma before a closing brace or bracket
        while (i >= 0 && jsonStr.charAt(i) == ',') {
            i--;
        }
        
        // If no comma found, return the original string
        if (i < 0) {
            return jsonStr;
        }
        
        // Check if the next character is a closing brace or bracket
        if (i + 1 < n && (jsonStr.charAt(i + 1) == '}' || jsonStr.charAt(i + 1) == ']')) {
            // Remove the comma and the closing brace or bracket
            return jsonStr.substring(0, i) + jsonStr.substring(i + 2);
        }
        
        // If the comma is not followed by a closing brace or bracket, return the original string
        return jsonStr;
    }
}