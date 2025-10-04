public class Tested {
    /**
     * Concatenates two integer arrays into a single array. If either of the input arrays is empty,
     * the method returns the non-empty array. If both arrays are empty, an empty array is returned.
     *
     * @param array1 the first array to concatenate; must not be null
     * @param array2 the second array to concatenate; must not be null
     * @return a new array containing all elements from {@code array1} followed by all elements from {@code array2}.
     *         If {@code array1} is empty, {@code array2} is returned. If {@code array2} is empty, {@code array1} is returned.
     *         If both arrays are empty, an empty array is returned.
     * @throws NullPointerException if either {@code array1} or {@code array2} is null
     */
    public static int[] concat(int[] array1, int[] array2) {
        // Check for null values
        if (array1 == null || array2 == null) {
            throw new NullPointerException("Arrays cannot be null");
        }

        // Create a new array to hold the result
        int[] result = new int[array1.length + array2.length];

        // Copy elements from array1 to result
        System.arraycopy(array1, 0, result, 0, array1.length);

        // Copy elements from array2 to result
        System.arraycopy(array2, 0, result, array1.length, array2.length);

        return result;
    }
}