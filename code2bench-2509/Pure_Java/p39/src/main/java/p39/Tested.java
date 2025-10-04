package p39;

import java.util.regex.Pattern;

public class Tested {
    /**
     * Removes all non-printable characters from the given string, preserving newlines (`\\n`), 
     * carriage returns (`\\r`), and tabs (`\\t`). Printable characters are defined as those 
     * matching the Unicode `\\p{Print}` character class.
     *
     * <p>If the input string is {@code null}, this method returns {@code null}.
     *
     * @param str the input string from which non-printable characters are to be removed. 
     *            May be {@code null}.
     * @return the input string with all non-printable characters removed, or {@code null} 
     *         if the input string is {@code null}.
     */
    public static String removeNonPrintableCharacters(String str) {
        if (str == null)
            return null;
        return str.replaceAll("[^\\n\\r\\t\\p{Print}]", "");
    }
}