public class Tested {
    /**
     * Copies the specified range of the specified byte array into a new array. The initial
     * index of the range (from) must lie between zero and original.length, inclusive. The
     * value at original[from] is placed into the initial element of the copy (unless
     * from == original.length or from == to). Values from subsequent elements in the
     * original array are placed into subsequent elements in the copy. The final index of
     * the range (to), which must be greater than or equal to from, may be greater than
     * original.length, in which case the copy will be padded with zeros.
     *
     * @param original the array from which a range is to be copied
     * @param from the initial index of the range to be copied, inclusive
     * @param to the final index of the range to be copied, exclusive
     * @return a new array containing the specified range from the original array,
     *         truncated or padded with zeros to obtain the required length
     * @throws IllegalArgumentException if from > to
     * @throws NullPointerException if original is null
     */
    public static byte[] copyOfRange(byte[] original, int from, int to) {
        if (original == null) {
            throw new NullPointerException("original cannot be null");
        }
        if (from > to) {
            throw new IllegalArgumentException("from must be <= to");
        }
        if (from < 0 || to > original.length) {
            throw new IllegalArgumentException("from and to must be within bounds");
        }
        
        int length = to - from;
        byte[] result = new byte[length];
        System.arraycopy(original, from, result, 0, length);
        return result;
    }
}