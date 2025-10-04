package p247;

import java.util.*;

public class Tested {
    /**
     * Counts the number of newline characters ('\n') in the given string.
     *
     * <p>This method iterates through each character of the string and increments a counter
     * whenever a newline character is encountered. The method is case-sensitive and only
     * counts the exact newline character '\n'.
     *
     * @param str The string to be analyzed. If {@code null}, the method returns 0.
     * @return The number of newline characters in the string. Returns 0 if the string is
     *         {@code null} or contains no newline characters.
     */
    public static int countNewLines(String str) {
        if (str == null) {
            return 0;
        }
        
        int count = 0;
        for (int i = 0; i < str.length(); i++) {
            if (str.charAt(i) == '\n') {
                count++;
            }
        }
        return count;
    }
}