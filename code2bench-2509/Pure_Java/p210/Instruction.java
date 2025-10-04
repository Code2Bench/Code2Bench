package p210;

public class Tested {
    /**
     * Calculates the entropy of a byte array based on the frequency of byte value changes.
     * The entropy is computed as the ratio of the number of transitions between distinct byte values
     * to the total number of possible transitions (i.e., the length of the array minus one).
     *
     * <p>For example, given the byte array {@code [1, 1, 2, 2, 3]}, the entropy would be calculated as
     * 2 transitions (1 → 2 and 2 → 3) divided by 4 possible transitions, resulting in 0.5.
     *
     * @param bytes the byte array to calculate entropy for; must not be null or empty
     * @return the entropy value as a double between 0.0 and 1.0, inclusive
     * @throws IllegalArgumentException if the input array is null or empty
     */
    public static double entropy(byte[] bytes) {
        // TODO: implement this method
    }
}