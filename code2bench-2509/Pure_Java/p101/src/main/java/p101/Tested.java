package p101;

import java.util.*;

public class Tested {
    /**
     * Rounds the given number of bytes to the nearest multiple of 8 (i.e., the nearest word boundary).
     * If the number of bytes is already a multiple of 8, it is returned unchanged. Otherwise, the
     * method calculates the smallest multiple of 8 that is greater than or equal to the input.
     *
     * @param numBytes The number of bytes to round. Must be a non-negative integer.
     * @return The rounded number of bytes, which is the nearest multiple of 8.
     */
    protected static int roundNumberOfBytesToNearestWord(int numBytes) {
        // If the number is already a multiple of 8, return it as is
        if (numBytes % 8 == 0) {
            return numBytes;
        }
        
        // Otherwise, calculate the next multiple of 8
        int remainder = numBytes % 8;
        return numBytes + (8 - remainder);
    }
}