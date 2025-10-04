public class Tested {
    /**
     * Copies elements from the specified 'toIndex' to the end of the array, overwriting elements starting at 'fromIndex'.
     * The method ensures that the indices are within the bounds of the array and that 'fromIndex' is not greater than 'toIndex'.
     * If any of these conditions are not met, the method returns the original length of the array without performing any copy operation.
     *
     * @param array The array from which elements are copied and overwritten. Must not be null.
     * @param fromIndex The starting index in the array where elements will be overwritten. Must be less than or equal to 'toIndex' and within the array bounds.
     * @param toIndex The starting index in the array from which elements will be copied. Must be within the array bounds.
     * @return The new length of the array after the copy operation, or the original length if no copy operation was performed.
     * @throws NullPointerException if the array is null.
     */
    public static int copyOverWrite(float[] array, int fromIndex, int toIndex) {
        if (array == null) {
            throw new NullPointerException("array cannot be null");
        }

        // Check if fromIndex is not greater than toIndex
        if (fromIndex > toIndex) {
            return array.length;
        }

        // Check if indices are within bounds
        if (fromIndex < 0 || toIndex >= array.length) {
            return array.length;
        }

        // Copy elements from 'toIndex' to the end of the array
        System.arraycopy(array, toIndex, array, fromIndex, array.length - toIndex);

        return array.length;
    }
}