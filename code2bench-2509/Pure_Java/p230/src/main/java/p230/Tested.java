public class Tested {
    /**
     * Expands the given boolean array by adding a specified number of elements and optionally shifting the original elements.
     * The new elements are added either at the beginning or the end of the array, depending on the value of the {@code flag} parameter.
     *
     * @param objs The original boolean array to be expanded. Must not be null.
     * @param i The number of elements to add to the array. Must be non-negative.
     * @param flag If {@code true}, the original elements are shifted to the end of the new array, leaving the new elements at the beginning.
     *             If {@code false}, the original elements are kept at the beginning of the new array, leaving the new elements at the end.
     * @return A new boolean array containing the original elements and the additional elements. The length of the new array is {@code objs.length + i}.
     * @throws NullPointerException if {@code objs} is {@code null}.
     * @throws IllegalArgumentException if {@code i} is negative.
     */
    public static boolean[] expand(boolean[] objs, int i, boolean flag) {
        if (objs == null) {
            throw new NullPointerException("objs cannot be null");
        }
        if (i < 0) {
            throw new IllegalArgumentException("i must be non-negative");
        }

        boolean[] result = Arrays.copyOf(objs, objs.length + i);
        if (flag) {
            System.arraycopy(objs, 0, result, result.length - i, objs.length);
        } else {
            System.arraycopy(objs, 0, result, 0, objs.length);
        }
        return result;
    }
}