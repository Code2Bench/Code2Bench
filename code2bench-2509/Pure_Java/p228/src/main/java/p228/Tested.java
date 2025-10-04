public class Tested {
    /**
     * Expands the given array of strings by adding additional elements at the beginning or end,
     * depending on the specified flag. The original elements are copied into the new array,
     * either starting at the beginning (if {@code flag} is {@code true}) or offset by {@code i}
     * positions (if {@code flag} is {@code false}). The new array will have a length of
     * {@code objs.length + i}.
     *
     * @param objs The original array of strings to be expanded. Must not be {@code null}.
     * @param i The number of additional elements to add to the array. Must be non-negative.
     * @param flag If {@code true}, the original elements are copied to the beginning of the new array.
     *             If {@code false}, the original elements are copied starting at index {@code i}.
     * @return A new array of strings with the expanded size, containing the original elements
     *         in the specified position.
     * @throws NullPointerException if {@code objs} is {@code null}.
     * @throws IllegalArgumentException if {@code i} is negative.
     */
    public static String[] expand(String[] objs, int i, boolean flag) {
        if (objs == null) {
            throw new NullPointerException("objs cannot be null");
        }
        if (i < 0) {
            throw new IllegalArgumentException("i must be non-negative");
        }

        int newSize = objs.length + i;
        String[] result = new String[newSize];

        if (flag) {
            // Copy original elements to the beginning
            System.arraycopy(objs, 0, result, 0, objs.length);
        } else {
            // Copy original elements starting at index i
            System.arraycopy(objs, i, result, 0, objs.length);
        }

        return result;
    }
}