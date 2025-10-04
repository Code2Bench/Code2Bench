package p148;

import java.util.regex.Pattern;

public class Tested {
    /**
     * Cleans and normalizes a given string, typically used for version strings. The method performs the following steps:
     * 1. If the input string is null or empty, returns an empty string.
     * 2. Trims leading and trailing whitespace and converts the string to lowercase.
     * 3. If the resulting string starts with the character 'v', removes the 'v' from the beginning.
     * 4. Replaces all hyphens ('-') with periods ('.') to treat package versions as part of the version string.
     *
     * @param str The input string to be cleaned. Can be null or empty.
     * @return A cleaned and normalized version of the input string. Returns an empty string if the input is null or empty.
     */
    private static String clean(String str) {
        if (str == null || str.isEmpty()) {
            return "";
        }
        
        // Trim whitespace and convert to lowercase
        String trimmed = str.trim().toLowerCase();
        
        // Remove 'v' if present
        if (trimmed.startsWith("v")) {
            trimmed = trimmed.substring(1);
        }
        
        // Replace hyphens with periods
        String normalized = trimmed.replace('-', '.');
        
        return normalized;
    }
}