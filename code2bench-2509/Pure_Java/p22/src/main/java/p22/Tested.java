package p22;

import java.util.*;

public class Tested {
    /**
     * Splits the given source string into an array of substrings, each of the specified length.
     * The last substring may be shorter than the specified length if the source string's length
     * is not a multiple of the specified length.
     *
     * @param src the source string to be split. Must not be null.
     * @param length the length of each substring. Must be a positive integer.
     * @return an array of substrings derived from the source string. The array will have
     *         a length equal to the ceiling of the source string's length divided by the specified length.
     * @throws IllegalArgumentException if the length is less than or equal to 0.
     * @throws NullPointerException if the source string is null.
     */
    public static String[] stringToStringArray(String src, int length) {
        if (src == null) {
            throw new NullPointerException("Source string cannot be null");
        }
        if (length <= 0) {
            throw new IllegalArgumentException("Length must be a positive integer");
        }

        int totalLength = src.length();
        int numberOfSubstrings = (int) Math.ceil((double) totalLength / length);

        String[] result = new String[numberOfSubstrings];
        for (int i = 0; i < numberOfSubstrings; i++) {
            int startIndex = i * length;
            int endIndex = startIndex + length;
            if (endIndex > totalLength) {
                endIndex = totalLength;
            }
            result[i] = src.substring(startIndex, endIndex);
        }

        return result;
    }
}