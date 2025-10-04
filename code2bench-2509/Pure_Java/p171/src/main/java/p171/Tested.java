package p171;

import java.util.*;

public class Tested {
    /**
     * Checks whether the upper half bits (bits 4-7) of the modified integer have been flipped
     * compared to the original integer. The method masks both integers with 0xF0 (binary 11110000)
     * to isolate the upper half bits and then performs an XOR operation to determine if any bits
     * in this range have changed.
     *
     * @param original The original integer value to compare.
     * @param modified The modified integer value to compare against the original.
     * @return {@code true} if any of the upper half bits (bits 4-7) have been flipped in the
     *         modified integer compared to the original; {@code false} otherwise.
     */
    private static boolean checkUpperHalfBitsFlipped(int original, int modified) {
        // Mask to isolate upper half bits (bits 4-7)
        int mask = 0xF0;
        
        // Get the upper half bits from both integers
        int upperOriginal = original & mask;
        int upperModified = modified & mask;
        
        // Check if any bits in the upper half have changed
        return (upperOriginal ^ upperModified) != 0;
    }
}