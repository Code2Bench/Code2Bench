package p78;

import java.util.StringTokenizer;

public class Tested {
    /**
     * Trims trailing whitespace characters from the given string. This method scans the string
     * from the end towards the beginning, removing any whitespace characters (as determined by
     * {@link Character#isWhitespace(char)}) until a non-whitespace character is encountered or
     * the beginning of the string is reached.
     *
     * <p>If the input string is empty or consists solely of whitespace characters, an empty string
     * is returned.
     *
     * @param s the string to trim; must not be null
     * @return a new string with trailing whitespace removed; never null
     * @throws NullPointerException if the input string {@code s} is null
     */
    public static String rtrim(String s) {
        if (s == null) {
            throw new NullPointerException("Input string cannot be null");
        }
        
        int len = s.length();
        if (len == 0) {
            return "";
        }
        
        // Start from the end of the string
        int i = len - 1;
        
        // Trim whitespace from the end
        while (i >= 0 && Character.isWhitespace(s.charAt(i))) {
            i--;
        }
        
        // Return the substring from 0 to i+1
        return s.substring(0, i + 1);
    }
}