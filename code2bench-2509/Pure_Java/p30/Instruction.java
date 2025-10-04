package p30;

import java.util.*;

public class Tested {
    /**
     * Splits the input string into segments of the specified length and inserts the given split string
     * between them. The method ensures that only segments of the exact specified length are included
     * in the final result, with the split string appended after each segment.
     *
     * <p>For example, given the input string "123456789", a split string of "-", and a length of 3,
     * the method will return "123-456-789".
     *
     * @param str    the input string to be split. Must not be null.
     * @param split  the string to insert between segments. Must not be null.
     * @param length the length of each segment. Must be a positive integer.
     * @return a string containing the segments of the specified length, separated by the split string.
     * @throws IllegalArgumentException if {@code length} is less than or equal to 0.
     * @throws NullPointerException if {@code str} or {@code split} is null.
     */
    public static String getSplitString(String str, String split, int length) {
        // TODO: implement this method
    }
}