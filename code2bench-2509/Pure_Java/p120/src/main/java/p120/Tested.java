package p120;

import java.util.Optional;

public class Tested {
    /**
     * Extracts the title portion from a full title string that may contain a colon separator.
     * The method splits the input string at the first occurrence of a colon and returns the
     * trimmed portion before the colon. If the input string is null, the method returns null.
     *
     * @param fullTitle The full title string from which to extract the title. May be null.
     * @return The extracted title portion, trimmed of leading and trailing whitespace, or null
     *         if the input string is null.
     */
    public static String extractTitleFromFull(String fullTitle) {
        if (fullTitle == null) {
            return null;
        }
        
        int colonIndex = fullTitle.indexOf(':');
        if (colonIndex != -1) {
            return fullTitle.substring(0, colonIndex).trim();
        }
        
        return fullTitle.trim();
    }
}