package p85;

import java.util.Arrays;

public class Tested {
    /**
     * Copies the specified range of the specified byte array into a new array.
     * The initial index of the range (from) must lie between zero and original.length, inclusive.
     * The final index of the range (to) must be greater than or equal to from.
     * The final index may be greater than original.length, in which case the copy will be padded with zeros.
     *
     * @param original the array from which a range is to be copied
     * @param from the initial index of the range to be copied, inclusive
     * @param to the final index of the range to be copied, exclusive
     * @return a new array containing the specified range from the original array, truncated or padded with zeros to obtain the required length
     * @throws IllegalArgumentException if from > to
     * @throws NullPointerException if the original array is null
     */
    public static byte[] copyOfRange(byte[] original, int from, int to) {
        // TODO: implement this method
    }
}