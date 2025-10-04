package p273;

import java.util.stream.Collectors;

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
        // Check for null or empty code
        if (code == null || code.isEmpty()) {
            throw new IllegalArgumentException("Code cannot be null or empty");
        }

        // Check for non-digit characters
        if (!code.matches("\\d+")) {
            throw new IllegalArgumentException("Code must contain only digits");
        }

        // Calculate the weighted sum
        int weightedSum = 0;
        for (int i = code.length() - 1; i >= 0; i--) {
            int digit = Character.getNumericValue(code.charAt(i));
            if (i % 2 == 0) {
                weightedSum += digit * 3;
            } else {
                weightedSum += digit * 1;
            }
        }

        // Determine the parity digit
        int parityDigit = 10 - (weightedSum % 10);
        if (parityDigit == 0) {
            return 0;
        }
        return parityDigit;
    }
}