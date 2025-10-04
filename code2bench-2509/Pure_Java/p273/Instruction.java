package p273;

public class Tested {
    /**
     * Calculates the parity digit for an EAN (European Article Number) code.
     * The method computes the parity digit by iterating over the characters of the code,
     * starting from the end, and applying a weighted sum. The weights alternate between
     * 3 and 1 for each character. The parity digit is then determined as the smallest
     * non-negative integer that, when added to the weighted sum, results in a multiple of 10.
     *
     * param code The EAN code as a string, excluding the parity digit. Must not be null or empty.
     *            Each character in the string must be a digit (0-9).
     * return The calculated parity digit as an integer between 0 and 9.
     * throws IllegalArgumentException if the code is null, empty, or contains non-digit characters.
     */
    public static int calculateEANParity(String code) {
        // TODO: implement this method
    }
}