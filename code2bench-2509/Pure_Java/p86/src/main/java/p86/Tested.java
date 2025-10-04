public class Tested {
    /**
     * Copies the specified range of the specified byte array into a new array.
     * The initial index of the range (from) must lie between zero and original.length, inclusive.
     * The final index of the range (to) must be greater than or equal to from. It may be greater than
     * original.length, in which case the resulting array will have trailing zeros.
     *
     * @param original the array from which a range is to be copied
     * @param from the initial index of the range to be copied, inclusive
     * @param to the final index of the range to be copied, exclusive
     * @return a new array containing the specified range from the original array, truncated or padded with zeros to obtain the required length
     * @throws IllegalArgumentException if from > to or if from < 0
     * @throws NullPointerException if the original array is null
     */
    public static byte[] copyOfRange(byte[] original, int from, int to) {
        if (original == null) {
            throw new NullPointerException("original cannot be null");
        }
        if (from < 0 || to > original.length) {
            throw new IllegalArgumentException("from must be >= 0 and to must be <= original.length");
        }
        if (from >= to) {
            throw new IllegalArgumentException("from must be < to");
        }

        int length = to - from;
        byte[] result = new byte[length];

        System.arraycopy(original, from, result, 0, length);
        return result;
    }
}