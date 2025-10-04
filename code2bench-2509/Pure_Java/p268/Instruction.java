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
        // TODO: implement this method
    }
}