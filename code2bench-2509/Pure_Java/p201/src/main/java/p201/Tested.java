package p201;

import java.util.BitSet;

public class Tested {
    /**
     * Calculates the base-2 logarithm of the given integer, rounded down to the nearest integer.
     * The method uses a series of bitwise operations to efficiently determine the highest set bit
     * in the input value, which corresponds to the logarithm.
     *
     * @param in The input integer for which to calculate the base-2 logarithm. Must be a positive integer.
     * @return The base-2 logarithm of the input, rounded down to the nearest integer. Returns 0 if the input is 0.
     */
    public static int log2(int in) {
        if (in == 0) {
            return 0;
        }
        
        // Find the highest set bit using bitwise operations
        int highestBit = 0;
        while ((in & (1 << highestBit)) != 0) {
            highestBit++;
        }
        
        return highestBit - 1;
    }
}