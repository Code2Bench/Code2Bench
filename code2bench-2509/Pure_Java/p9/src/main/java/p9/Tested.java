package p9;

import java.util.regex.Pattern;

public class Tested {
    /**
     * Cleans the input text by removing HTML tags and excess whitespace.
     * 
     * This method is not yet implemented. When implemented, it will perform the following operations in sequence:
     * 1. If the input text is null, it will return null.
     * 2. Remove all HTML tags using a regular expression.
     * 3. Replace sequences of one or more whitespace characters with a single space.
     * 4. Trim leading and trailing whitespace from the resulting string.
     *
     * @param text The input text to be cleaned. Can be null.
     * @return The cleaned text with HTML tags and excess whitespace removed. Returns null if the input text is null.
     */
    public static String cleanText(String text) {
        if (text == null) {
            return null;
        }
        
        // Step 2: Remove all HTML tags using a regular expression
        String htmlTagRegex = "<[^>]*>";
        String cleanedText = text.replaceAll(htmlTagRegex, "");
        
        // Step 3: Replace sequences of one or more whitespace characters with a single space
        cleanedText = cleanedText.replacePattern(" +", " ");
        
        // Step 4: Trim leading and trailing whitespace
        cleanedText = cleanedText.trim();
        
        return cleanedText;
    }
}