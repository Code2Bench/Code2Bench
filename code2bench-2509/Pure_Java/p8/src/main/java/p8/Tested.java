package p8;

import java.util.Objects;

public class Tested {
    /**
     * Extracts the first JSON object from the given text. A JSON object is defined as a substring
     * that starts with '{' and ends with the matching '}'. The method handles nested JSON objects
     * by counting the braces to ensure the correct closing brace is found.
     *
     * <p>If no JSON object is found in the text, an empty JSON object "{}" is returned.
     *
     * <p><b>Note:</b> This method is not yet implemented and contains a TODO placeholder.
     *
     * @param text the input text from which to extract the JSON object. If null, an empty JSON
     *             object "{}" is returned.
     * @return the first JSON object found in the text as a String, or "{}" if no JSON object is found.
     */
    public static String extractFirstJsonObject(String text) {
        if (text == null) {
            return "{}";
        }

        int openBraces = 0;
        int closeBraces = 0;
        int start = 0;

        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if (c == '{') {
                openBraces++;
            } else if (c == '}') {
                closeBraces++;
            }

            if (openBraces == closeBraces) {
                // Found a matching closing brace
                start = i;
                break;
            }
        }

        if (start == text.length()) {
            return "{}";
        }

        // Extract the substring from start to the matching closing brace
        return text.substring(start, start + 2 + closeBraces);
    }
}