package p250;
public class GroundTruth {
    public static int calculateSpacesForAlignment(int currentWidth, int targetPosition, int spaceWidth) {
        // Calculate space needed in pixels
        int pixelsNeeded = targetPosition - currentWidth;

        // Calculate spaces needed (with minimum of 1 space for separation)
        if (pixelsNeeded <= 0) {
            return 1; // Ensure at least one space between columns
        }

        // Calculate the exact number of spaces needed
        int spaces = (int)Math.ceil((double)pixelsNeeded / spaceWidth);

        // Cap at a reasonable maximum
        return Math.min(spaces, 100);
    }
}