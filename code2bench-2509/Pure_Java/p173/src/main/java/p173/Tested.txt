package p173;

import java.util.Objects;

public class Tested {
    /**
     * Converts the given input object into a {@code long[]} array. The method supports
     * conversion from {@code int[]} and {@code long[]} input types. If the input is an
     * {@code int[]}, each element is cast to a {@code long} and stored in the resulting
     * array. If the input is already a {@code long[]}, it is returned directly. For all
     * other input types, the method returns {@code null}.
     *
     * @param inputObj the input object to convert, which must be either an {@code int[]}
     *                 or a {@code long[]}. Other types will result in a {@code null} return.
     * @return a {@code long[]} array containing the converted values, or {@code null} if
     *         the input is not an {@code int[]} or {@code long[]}.
     * @throws NullPointerException if {@code inputObj} is {@code null}.
     */
    public static long[] convertToLongArray(Object inputObj) {
        // TODO: implement this method
    }
}