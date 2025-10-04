package p13;

import java.util.Objects;

public class Tested {
    /**
     * Cleans a raw JSON string by trimming whitespace and extracting the content between the first '{' and the last '}'.
     * If the input string does not contain a valid JSON object (i.e., it lacks a '{' or '}' or they are in the wrong order),
     * an empty string is returned.
     *
     * @param rawJsonString the raw JSON string to be cleaned; may be null or empty
     * @return the cleaned JSON string, or an empty string if the input does not contain a valid JSON object
     */
    public static String cleanJsonString(String rawJsonString) {
        if (rawJsonString == null || rawJsonString.isEmpty()) {
            return "";
        }

        int openBrace = rawJsonString.indexOf('{');
        int closeBrace = rawJsonString.lastIndexOf('}');

        if (openBrace == -1 || closeBrace == -1 || openBrace > closeBrace) {
            return "";
        }

        // Trim whitespace from start and end
        String trimmed = rawJsonString.trim();
        // Extract the content between first '{' and last '}'
        String cleaned = trimmed.substring(openBrace + 1, closeBrace);

        return cleaned;
    }
}