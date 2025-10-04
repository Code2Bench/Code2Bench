public class Tested {
    /**
     * Copies the specified range of the given byte array into a new array. The range is defined
     * by the {@code from} index (inclusive) and the {@code to} index (exclusive). The length of
     * the new array will be {@code to - from}. If {@code from} is greater than {@code to}, an
     * {@code IllegalArgumentException} is thrown.
     *
     * <p>If the range exceeds the bounds of the original array, the copy will contain as many
     * elements as possible, up to the length of the original array minus the {@code from} index.
     *
     * @param original the array from which a range is to be copied
     * @param from the initial index of the range to be copied, inclusive
     * @param to the final index of the range to be copied, exclusive
     * @return a new array containing the specified range from the original array
     * @throws IllegalArgumentException if {@code from} is greater than {@code to}
     * @throws NullPointerException if {@code original} is {@code null}
     */
    public static byte[] copyOfRange(byte[] original, int from, int to) {
        if (original == null) {
            throw new NullPointerException("original cannot be null");
        }
        if (from > to) {
            throw new IllegalArgumentException("from cannot be greater than to");
        }
        
        int length = to - from;
        byte[] result = new byte[length];
        System.arraycopy(original, from, result, 0, length);
        return result;
    }
}