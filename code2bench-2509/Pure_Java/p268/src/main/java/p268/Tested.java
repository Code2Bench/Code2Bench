package p268;

import java.util.Objects;

public class Tested {
    /**
     * Finds the starting index of the first occurrence of the specified {@code needle} byte array
     * within the {@code hay} byte array, starting the search from the specified {@code from} index.
     * 
     * <p>The method performs a linear search, comparing each byte of the {@code needle} array with
     * the corresponding bytes in the {@code hay} array. If a mismatch is found, the search continues
     * from the next position in the {@code hay} array. If a complete match is found, the starting
     * index of the match is returned.
     *
     * @param hay the byte array to search within; must not be {@code null}
     * @param needle the byte array to search for; must not be {@code null}
     * @param from the index in the {@code hay} array to start the search from; must be non-negative
     * @return the starting index of the first occurrence of {@code needle} in {@code hay}, or
     *         {@code -1} if no match is found or if {@code needle} is empty
     * @throws NullPointerException if either {@code hay} or {@code needle} is {@code null}
     * @throws IllegalArgumentException if {@code from} is negative or if {@code from} is greater than
     *         the length of {@code hay} minus the length of {@code needle}
     */
    private static int indexOf(byte[] hay, byte[] needle, int from) {
        if (needle == null || hay == null) {
            throw new NullPointerException("hay or needle cannot be null");
        }
        
        if (needle.length == 0) {
            return -1;
        }
        
        if (from < 0 || from > hay.length - needle.length) {
            throw new IllegalArgumentException("Invalid start index");
        }
        
        for (int i = from; i < hay.length; i++) {
            if (i + needle.length > hay.length) {
                break;
            }
            boolean match = true;
            for (int j = 0; j < needle.length; j++) {
                if (hay[i + j] != needle[j]) {
                    match = false;
                    break;
                }
            }
            if (match) {
                return i;
            }
        }
        return -1;
    }
}