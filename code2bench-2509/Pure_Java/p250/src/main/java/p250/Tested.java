package p250;

public class Tested {
    /**
     * Calculates the number of spaces required to align text to a target position, given the current width,
     * target position, and the width of a single space. The method ensures a minimum of one space for separation
     * and caps the result at a reasonable maximum of 100 spaces.
     *
     * @param currentWidth The current width of the text in pixels. Must be a non-negative integer.
     * @param targetPosition The target position to align the text to in pixels. Must be a non-negative integer.
     * @param spaceWidth The width of a single space character in pixels. Must be a positive integer.
     * @return The number of spaces required for alignment, ensuring at least one space and capped at 100.
     */
    public static int calculateSpacesForAlignment(int currentWidth, int targetPosition, int spaceWidth) {
        // Calculate the number of spaces needed
        int spaces = (targetPosition - currentWidth) / spaceWidth;
        
        // Ensure at least one space
        if (spaces <= 0) {
            spaces = 1;
        }
        
        // Cap at 100 spaces
        if (spaces > 100) {
            spaces = 100;
        }
        
        return spaces;
    }
}