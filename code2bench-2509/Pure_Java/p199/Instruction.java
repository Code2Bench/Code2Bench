package p199;

import java.util.Objects;

public class Tested {
    /**
     * Parses a string of space-separated integers into an array of integers.
     *
     * <p>The input string is expected to contain integers separated by single spaces. Each substring
     * between spaces is parsed as an integer using {@link Integer#parseInt(String)}. The resulting
     * array has the same length as the number of integers in the input string.
     *
     * <p>If the input string is {@code null}, a {@code NullPointerException} is thrown. If any substring
     * cannot be parsed as an integer, a {@code NumberFormatException} is thrown.
     *
     * @param s the string containing space-separated integers to parse; must not be {@code null}
     * @return an array of integers parsed from the input string
     * @throws NullPointerException if the input string is {@code null}
     * @throws NumberFormatException if any substring cannot be parsed as an integer
     */
    private static int[] parseIntegerArray(String s) {
        // TODO: implement this method
    }
}