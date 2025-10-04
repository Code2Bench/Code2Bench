package p253;

import java.lang.Integer;

public class Tested {
    /**
     * Extracts the Y-coordinate from a chunk block index.
     *
     * <p>The method interprets the input index as a packed value where the Y-coordinate is stored
     * in bits 4-28. The sign of the Y-coordinate is determined by bit 28 (0x08000000). If bit 28 is set,
     * the Y-coordinate is negative; otherwise, it is positive.
     *
     * @param index The chunk block index containing the packed Y-coordinate. The Y-coordinate is stored
     *              in bits 4-28, and the sign is determined by bit 28.
     * @return The extracted Y-coordinate, which can be positive or negative depending on the sign bit.
     */
    public static int chunkBlockIndexGetY(int index) {
        // Extract the Y-coordinate from the index
        int y = (index >> 4) & 0xFFFFFFF;
        
        // Check the sign bit (bit 28)
        boolean isNegative = (y & 0x08000000) != 0;
        
        // Return the Y-coordinate with proper sign
        return isNegative ? -y : y;
    }
}