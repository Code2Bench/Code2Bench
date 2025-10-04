package p102;

import java.util.*;

public class Tested {
    /**
     * Rounds the given number of bytes to the nearest multiple of 8 (a word boundary).
     * If the number of bytes is already a multiple of 8, it is returned unchanged.
     * Otherwise, the number of bytes is increased to the next multiple of 8.
     *
     * @param numBytes The number of bytes to round. Must be a non-negative integer.
     * @return The number of bytes rounded to the nearest multiple of 8.
     * @throws IllegalArgumentException if {@code numBytes} is negative.
     */
    protected static int roundNumberOfBytesToNearestWord(int numBytes) {
        if (numBytes < 0) {
            throw new IllegalArgumentException("numBytes must be non-negative");
        }
        
        // Calculate the nearest multiple of 8
        int remainder = numBytes % 8;
        if (remainder == 0) {
            return numBytes;
        } else {
            return numBytes + (8 - remainder);
        }
    }
}