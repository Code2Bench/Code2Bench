public class Tested {
    /**
     * Expands the given float array by adding a specified number of elements and returns the new array.
     * The original array elements are copied into the new array, either at the beginning or after the
     * specified number of new elements, depending on the flag.
     *
     * @param objs The original float array to be expanded. Must not be null.
     * @param i The number of elements to add to the array. Must be non-negative.
     * @param flag If true, the original array elements are copied to the beginning of the new array.
     *             If false, the original array elements are copied after the specified number of new elements.
     * @return A new float array with the expanded size, containing the original elements in the specified position.
     * @throws IllegalArgumentException if {@code i} is negative.
     * @throws NullPointerException if {@code objs} is null.
     */
    public static float[] expand(float[] objs, int i, boolean flag) {
        if (i < 0) {
            throw new IllegalArgumentException("Number of elements to add must be non-negative");
        }
        if (objs == null) {
            throw new NullPointerException("Original array cannot be null");
        }

        float[] result = Arrays.copyOf(objs, objs.length + i);
        if (flag) {
            System.arraycopy(objs, 0, result, 0, objs.length);
        } else {
            System.arraycopy(objs, 0, result, objs.length, i);
        }
        return result;
    }
}