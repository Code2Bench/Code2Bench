package p203;

public class Tested {
    /**
     * Converts a large number into a more readable, abbreviated format with a suffix indicating its magnitude.
     * The method scales the number down and appends a suffix based on its size:
     * - Numbers >= 10^18 are converted to "E" (exa) scale.
     * - Numbers >= 10^15 are converted to "P" (peta) scale.
     * - Numbers >= 10^12 are converted to "T" (tera) scale.
     * - Numbers >= 10^9 are converted to "G" (giga) scale.
     * - Numbers >= 10^6 are converted to "M" (mega) scale.
     * - Numbers >= 10^3 are converted to "k" (kilo) scale.
     * Numbers smaller than 10^3 are returned as-is without any suffix.
     * The result is rounded to two decimal places for scaled numbers.
     *
     * @param l The number to be converted. Must be a non-negative long value.
     * @return A string representation of the number in abbreviated format, or the original number as a string if it is less than 10^3.
     */
    public static String getShortNumber(long l) {
        // TODO: implement this method
    }
}