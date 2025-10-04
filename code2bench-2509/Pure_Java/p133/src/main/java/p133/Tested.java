package p133;

import java.util.*;

public class Tested {
    /**
     * Determines if the specified Unicode code point is a valid start for a Java identifier,
     * or if it is one of the special characters '@', '.', or '#'.
     *
     * <p>This method first converts the code point to a character and then checks if it is a valid
     * start for a Java identifier using {@link Character#isJavaIdentifierStart(int)}. Additionally,
     * it checks if the character is one of the special characters '@', '.', or '#'.
     *
     * @param codePoint the Unicode code point to be tested
     * @return {@code true} if the code point is a valid start for a Java identifier or is one of the
     *         special characters '@', '.', or '#'; {@code false} otherwise
     * @throws IllegalArgumentException if the specified code point is not a valid Unicode code point
     */
    public static boolean isValidIdentifierStart(int codePoint) {
        char ch = (char) codePoint;
        return Character.isJavaIdentifierStart(codePoint) || 
               (ch == '@' || ch == '.' || ch == '#');
    }
}