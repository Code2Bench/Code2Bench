package p84;

import java.util.Arrays;

public class Tested {
    /**
     * Copies the specified range of the given byte array into a new array. The range is defined
     * by the {@code from} (inclusive) and {@code to} (exclusive) indices. The length of the new
     * array will be {@code to - from}. If {@code from} is greater than {@code to}, an
     * {@code IllegalArgumentException} is thrown.
     *
     * <p>If the range exceeds the bounds of the original array, the copy will be truncated to
     * fit within the array's length. The method does not use {@code System.arraycopy} or
     * {@code Arrays.copyOf} to ensure compatibility in environments where these methods are
     * unavailable.
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