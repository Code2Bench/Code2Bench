package p89;

import java.util.Arrays;

public class Tested {
    /**
     * Copies the specified range of the given byte array into a new array. The range is defined
     * by the {@code from} index (inclusive) and the {@code to} index (exclusive). The length of
     * the new array will be {@code to - from}. If {@code from} is greater than {@code to}, an
     * {@code IllegalArgumentException} is thrown.
     *
     * <p>If the range extends beyond the length of the original array, the new array will be
     * filled only up to the end of the original array, and the remaining elements will be
     * uninitialized (i.e., zero).
     *
     * @param original the array from which a range is to be copied
     * @param from the initial index of the range to be copied, inclusive
     * @param to the final index of the range to be copied, exclusive
     * @return a new array containing the specified range from the original array
     * @throws IllegalArgumentException if {@code from} is greater than {@code to}
     * @throws NullPointerException if {@code original} is {@code null}
     */
    public static byte[] copyOfRange(byte[] original, int from, int to) {
        // TODO: implement this method
    }
}