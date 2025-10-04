public class Tested {
    /**
     * Concatenates two string arrays into a single array. If either of the input arrays is empty,
     * the other array is returned. If both arrays are empty, an empty array is returned.
     *
     * <p>This method efficiently handles the concatenation by using {@link System#arraycopy} to
     * copy elements from the input arrays into the result array.
     *
     * @param array1 the first string array to concatenate; may be empty but must not be null
     * @param array2 the second string array to concatenate; may be empty but must not be null
     * @return a new string array containing all elements from {@code array1} followed by all
     *         elements from {@code array2}; if either array is empty, the other array is returned
     * @throws NullPointerException if either {@code array1} or {@code array2} is null
     */
    public static String[] concat(String[] array1, String[] array2) {
        // Check for nulls
        if (array1 == null || array2 == null) {
            throw new NullPointerException("Cannot null array");
        }

        // Create a new array with the same size as the sum of the two arrays
        String[] result = new String[array1.length + array2.length];

        // Copy elements from array1 to result
        System.arraycopy(array1, 0, result, 0, array1.length);

        // Copy elements from array2 to result
        System.arraycopy(array2, 0, result, array1.length, array2.length);

        return result;
    }
}